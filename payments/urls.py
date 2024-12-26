# urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
	
    path('center/<int:center_pk>/membership/<int:membership_pk>/payment/',
        views.membership_payment_detail,
        name='membership_payment_detail'),
    path('center/<int:center_pk>/membership/payment/success/',
        views.membership_payment_success,
        name='membership_payment_success'),
	path('center/<int:center_pk>/membership/payment/fail/',
        views.membership_payment_fail,
        name='membership_payment_fail'),

    path('class/<int:class_pk>/classticket/<int:classticket_pk>/payment/',
        views.classticket_payment_detail,
        name='classticket_payment_detail'),
    path('class/<int:class_pk>/classticket/payment/success/',
        views.classticket_payment_success,
        name='classticket_payment_success'),
	path('class/<int:class_pk>/classticket/payment/fail/',
        views.classticket_payment_fail,
        name='classticket_payment_fail'),

		

]
