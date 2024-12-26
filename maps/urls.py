from django.urls import path
from . import views

urlpatterns = [
    path('', views.center_map, name='center_map'),
    
    
]