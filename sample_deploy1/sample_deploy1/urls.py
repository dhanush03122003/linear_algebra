from django.contrib import admin
from django.urls import path
from sample_app import views

urlpatterns = [
    path('hi/',views.HOME),
    path('display_det/',views.display_det),
    path('generate-excel/', views.generate_excel, name='generate-excel'),
    path('linear_algebra/',views.linear_alg),
]
