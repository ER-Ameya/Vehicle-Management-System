from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('list', views.vehicle_list, name='vehicle_list'),
    path('vehicle/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicle/new/', views.vehicle_new, name='vehicle_new'),
    path('vehicle/<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicle/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    # path('register/', views.register_vehicle, name='register_vehicle'),
    path('add_user/', views.add_user, name='add_user'),
    
]
