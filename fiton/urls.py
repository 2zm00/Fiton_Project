from django.contrib.auth.views import LoginView
from . import views
from django.urls import path,include


app_name ='fiton'

urlpatterns = [   
    path('signup/', views.signup, name='signup'),
    path('signup/choice/', views.signup_choice, name='signup_choice'),
    path('signup/done/', views.signup_done, name='signup_done'),
    path('signup/delete/', views.signup_delete, name='signup_delete'),
	
    ############## 프로필
    path('profile/user/<int:user_id>', views.profile_user, name='profile_user'),
    path('profile/user/<int:user_id>/modify', views.profile_modify, name='profile_modify'),
	
    ############## 센터
    path('center/', views.center, name='center'),
	path('center/<int:pk>/', views.center_detail, name='center_detail'),
	path('center/<int:pk>/register/', views.center_register, name='center_register'),
	path('center/<int:pk>/register/button/', views.center_register_button, name='center_register_button'),
	path('center/<int:pk>/register/delete/<int:instructor_id>', views.center_register_delete, name='center_register_delete'),
    path('center/<int:pk>/register/<str:status>', views.center_register_update, name='center_register_update'),

    ############## 강사
    path('instructor/list/', views.instructor_list, name='instructor_list'),
    path('instructor/detail/<int:user_id>', views.instructor_detail, name='instructor_detail'),

]
