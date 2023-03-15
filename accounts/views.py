from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegistrationForm, RoleForm
from user_management.models import UserProfile
from django.utils.html import escape
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# print(lambda u: u.u.userprofile.role == 'SA', lambda u: u.u.userprofile.role == 'A',lambda u: u.u.userprofile.role == 'U' )

@login_required
def home(request):
    user_role = UserProfile.objects.get(user =request.user.id).role
    return render(request, 'home.html', {'user_role': user_role})

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                try:
                    user_role = UserProfile.objects.get(user =request.user.id).role
                except UserProfile.DoesNotExist:
                    user_role = None
                if user_role == role:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator

# @login_required
# @role_required('SA')
def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid() :
            user = user_form.save()
            
            UserProfile.objects.create(user=user, role='U')
            # log the user in
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # redirect to user_list or some other page
            return redirect('accounts:user_list')
    else:
        user_form = RegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})

@login_required
def profile(request):
    
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        role_form = RoleForm(request.POST, instance=user_profile)
        if role_form.is_valid():
            role_form.save()
            return redirect('home')
    else:
        role_form = RoleForm(instance=user_profile)
    return render(request, 'profile.html', {'role_form': role_form})

@login_required
# @user_passes_test(lambda u: hasattr(u, 'userprofile') and (u.userprofile.role == 'SA' or u.userprofile.role == 'A'))

# @user_passes_test(lambda u :UserProfile.objects.get(user =1,role__in = ['SA','A']))

@user_passes_test(lambda u: UserProfile.objects.get(user =u.id).role == 'SA' or UserProfile.objects.get(user =u.id).role== 'A')
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: UserProfile.objects.get(user =u.id).role == 'SA' or UserProfile.objects.get(user =u.id).role== 'A')
def user_edit(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=user.u.userprofile)
        if form.is_valid():
            form.save()
            return redirect('accounts:user_list')
    else:
        # form = RoleForm(instance=user.u.userprofile)
        form = RoleForm(instance=UserProfile.objects.get(user =request.user.id))
    return render(request, 'accounts/user_edit.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = escape(request.POST.get('username'))
        password = escape(request.POST.get('password'))
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('vehicle_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')
