from django.contrib.auth.views import LoginView
from . import views
from django.urls import path,include


app_name ='fiton'

urlpatterns = [   
    path('signup/', views.signup, name='signup'),
    path('signup/choice/', views.signup_choice, name='signup_choice'),
    path('signup/done/', views.signup_done, name='signup_done'),
    path('signup/delete/', views.signup_delete, name='signup_delete'),
    #프로필
    path('profile/user/<int:user_id>', views.profile_user, name='profile_user'),
    path('profile/user/<int:user_id>/modify/', views.profile_modify, name='profile_modify'),


    #강사 url
    path('instructor/list/', views.instructor_list, name='instructor_list'),
    path('instructor/detail/<int:user_id>', views.instructor_detail, name='instructor_detail'),

]
