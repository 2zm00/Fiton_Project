# urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
	
    path('center/<int:center_pk>/payment/success/', 
        views.payment_success, 
        name='payment_success'),
		
    path('center/<int:center_pk>/payment/fail/', 
        views.payment_fail, 
        name='payment_fail'),
		
    path('center/<int:center_pk>/membership/purchase/<int:membership_pk>/payment/', views.payment_detail, name='payment_detail'),
]
