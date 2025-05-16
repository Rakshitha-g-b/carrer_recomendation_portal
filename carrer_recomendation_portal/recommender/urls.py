# File: C:\Users\LAPTOPS24\Desktop\New folder\career_guidance_system\recommender\urls.py

from django.urls import path
from . import views  # This is correct here, importing views from the recommender app

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('congratulations/', views.congratulations_view, name='congratulations'),
    path('college-search/', views.college_search_view, name='college_search'), # NEW
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # NEW for dynamic cities
]