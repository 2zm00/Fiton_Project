# urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('widget/<int:membership_id>/', views.payment_widget, name='widget'),
    path('success/', views.payment_success, name='success'),
    path('fail/', views.payment_fail, name='fail'),
]
