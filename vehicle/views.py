from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from .forms import VehicleForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import Group
from accounts.models import UserProfile
from accounts.forms import RegistrationForm, RoleForm



@login_required(login_url='login')
def vehicle_list(request):
    
    vehicle_list = Vehicle.objects.all()
    paginator = Paginator(vehicle_list, 10) # Show 10 vehicles per page
    page = request.GET.get('page')
    try:
        vehicles = paginator.page(int(page))
    except (TypeError, ValueError):
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)
    return render(request, 'vehicle/vehicle_list.html', {'page': page, 'vehicles': vehicles})


@login_required(login_url='login')
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    # user_group = Group.objects.filter(user=request.user).first() # get the user's group
    role = UserProfile.objects.get(user =request.user.id).role
    return render(request, 'vehicle/vehicle_detail.html', {'vehicle': vehicle, 'user_group': role})


@login_required(login_url='login')
def vehicle_new(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.save()
            # return redirect('vehicle_detail', pk=vehicle.pk)
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicle/vehicle_edit.html', {'form': form})


@login_required(login_url='login')
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.save()
            # return redirect('vehicle_detail', pk=vehicle.pk)
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicle/vehicle_edit.html', {'form': form})


@login_required(login_url='login')
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('vehicle_list')


def add_user(request):
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



