# File: C:\Users\LAPTOPS24\Desktop\New folder\career_guidance_system\config\urls.py

from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recommender.urls')),
]