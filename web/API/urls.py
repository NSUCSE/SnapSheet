from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import include, re_path

urlpatterns = [
    re_path('course_details_insert/', views.Insert_Course_Details),
    re_path('Add_Assessment/', views.Add_Assessment),
    re_path('Get_Users_Courses/', views.Get_Users_Courses),
]
