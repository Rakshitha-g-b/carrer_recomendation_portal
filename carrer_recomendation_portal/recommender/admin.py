# recommender/admin.py
from django.contrib import admin
from .models import State, City, College, StreamTag # Add Course if you defined it

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ('name',)

@admin.register(StreamTag)
class StreamTagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'website')
    list_filter = ('city', 'city__state', 'offered_streams')
    search_fields = ('name', 'city__name')
    filter_horizontal = ('offered_streams',) # Better UI for ManyToMany

# if you added the Course model:
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
# list_display = ('name', 'college', 'stream_tag')
# list_filter = ('college__city', 'stream_tag')
# search_fields = ('name', 'college__name')