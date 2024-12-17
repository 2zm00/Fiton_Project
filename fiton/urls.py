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

    path('class/', views.class_list, name='class_list'),
    path('class/open/', views.class_open, name='class_open'),

#     path('class/<int:class_pk>/modify/, views.cla #상세페이

#     path('class/<int:class_pk>/delete/, views.class_delete, name='class_delete'),
#     path('class/<int:class_pk> , views.class_detail  ,name='class_detail'),
]