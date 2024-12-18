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
	
    ############## 센터
    path('center/', views.center, name='center'),
	path('center/<int:pk>/', views.center_detail, name='center_detail'),
	path('center/<int:pk>/register/', views.center_register, name='center_register'),
	path('center/<int:pk>/register/delete/', views.center_register_delete, name='center_register_delete'),


    ############## 강사
    path('instructor/list/', views.instructor_list, name='instructor_list'),
    path('instructor/detail/<int:user_id>', views.instructor_detail, name='instructor_detail'),





    path('class/', views.class_list, name='class_list'),
    #URL타고 왔으니 여기서 TEMPLATE로 보내줄꺼야.
    path('class/<int:pk>/' , views.class_detail, name='class_detail'),
    path('class/open/', views.class_open, name='class_open'),
    path('class/<int:pk>/modify/',views.class_modify, name='class_modify'),
    path('class/<int:class_pk>/delete/', views.class_delete, name='class_delete'),
    path('class/<int:pk>/reserve', views.class_reserve, name='class_reserve'), #상세페이지 예약약

    #####리뷰
    path('class/<int:pk>/review' , views.class_review, name='class_review' ),
    
    path('class/<int:pk>/review/create', views.class_review_create, name='class_review_create'),
    path('class/<int:pk>/review/delete',views.class_review_delete,name='class_review_delete'),
    path('class/<int:pk>/review/modify', views.class_review_modify, name='class_review_modify'),
    # path('class/<int:pk>/category',views.class_category,name='class_category'),
    path('class/<int:pk>/price',views.class_price,name='class_price'),
    path('class/<int:pk>/info',views.class_info,name='class_info'),
    
]