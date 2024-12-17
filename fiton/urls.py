from django.contrib.auth.views import LoginView
from . import views
from django.urls import path,include


app_name ='fiton'

urlpatterns = [   
    path('signup/', views.signup, name='signup'),
    path('signup/choice/', views.signup_choice, name='signup_choice'),
    path('signup/done/', views.signup_done, name='signup_done'),
    path('signup/delete/', views.signup_delete, name='signup_delete'),
    path('profile/member/', views.profile_member, name='profile_member'),
    path('center/', views.center, name='center'),
	path('center/<int:pk>/', views.center_detail, name='center_detail'),
	path('center/<int:pk>/register/', views.center_register, name='center_register'),
	path('center/<int:pk>/register/delete/', views.center_register_delete, name='center_register_delete'),
]