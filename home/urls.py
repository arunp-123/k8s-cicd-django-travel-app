from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('booking/', views.booking, name="booking"),
    path('places/', views.places, name="places"),
    path('contact/', views.contact, name="contact"),

    
]