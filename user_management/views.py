from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import UserForm, UserProfileForm, EditProfileForm


@login_required
def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()
            # Set the password
            user.set_password(user.password)
            user.save()
            # Save the user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # Assign the user to the appropriate group based on their role
            role = profile.role
            if role == 'SA':
                group = Group.objects.get(name='Super Admin')
            elif role == 'A':
                group = Group.objects.get(name='Admin')
            else:
                group = Group.objects.get(name='User')
            group.user_set.add(user)
            # Redirect to the home page
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'user_management/register_user.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_profile(request):
    return render(request, 'user_management/view_profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('view_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'user_management/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password didn't match!")
            return redirect('change_password')
        if not request.user.check_password(old_password):
            messages.error(request, "Your old password was entered incorrectly. Please enter it again.")
            return redirect('change_password')
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Your password was successfully updated!')
        return redirect('view_profile')
    return render(request, 'user_management/change_password.html')

@login_required
def list_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'user_management/list_users.html', {'users': users})

@login_required
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user
            user = user_form.save()
            # Set the password
            user.set_password(user.password)
            user.save()
            # Save the user profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # Assign the user to the appropriate group based on their role
            role = profile.role
            if role == 'SA':
                group = Group.objects.get(name='Super Admin')
            elif role == 'A':
                group = Group.objects.get(name='Admin')
            else:
                group = Group.objects.get(name='User')
            group.user_set.add(user)
            messages.success(request, 'User was successfully created!')
            return redirect('list_users')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'user_management/create_user.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Assign the user to the appropriate group based on their role
            role = user.profile.role
            if role == 'SA':
                group = Group.objects.get(name='Super Admin')
            elif role == 'A':
                group = Group.objects.get(name='Admin')
            else:
                group = Group.objects.get(name='User')
            group.user_set.add(user)

