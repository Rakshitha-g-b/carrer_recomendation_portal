# recommender/admin.py
from django.contrib import admin
#from .models import State, City, College, StreamTag # Add Course if you defined it

# Better UI for ManyToMany

# if you added the Course model:
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
# list_display = ('name', 'college', 'stream_tag')
# list_filter = ('college__city', 'stream_tag')
# search_fields = ('name', 'college__name')