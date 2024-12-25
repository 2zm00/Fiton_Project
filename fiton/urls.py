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
    path('profile/user/<int:user_id>/myclass', views.myclass_list, name='myclass_list'),
	
    ############## 센터
    path('center/', views.center, name='center'),
	path('center/<int:pk>/', views.center_detail, name='center_detail'),
	path('center/<int:pk>/register/', views.center_register, name='center_register'),
	path('center/<int:pk>/register/button/', views.center_register_button, name='center_register_button'),
	path('center/<int:pk>/register/delete/<int:instructor_id>', views.center_register_delete, name='center_register_delete'),
    path('center/<int:pk>/register/<str:status>', views.center_register_update, name='center_register_update'),
	path('center/create', views.center_create, name='center_create'),

    ############## 강사
    path('instructor/list/', views.instructor_list, name='instructor_list'),
    path('instructor/detail/<int:user_id>', views.instructor_detail, name='instructor_detail'),

    ############## 멤버쉽(회원권)
	path('center/<int:pk>/membership/', views.membership_list, name='membership_list'),
	path('center/<int:center_pk>/membership/purchase/<int:membership_pk>/', views.membership_purchase, name='membership_purchase'),
	path('center/<int:center_pk>/membership/purchase/<int:membership_pk>/done', views.membership_purchase_done, name='membership_purchase_done'),
	path('center/<int:pk>/membership/create/', views.membership_create, name='membership_create'),
	path('center/<int:center_pk>/membership/<int:membership_pk>/', views.membership_detail, name='membership_detail'),
    path('center/<int:center_pk>/membership/<int:membership_pk>/modify', views.membership_modify, name='membership_modify'),
    path('center/<int:center_pk>/membership/<int:membership_pk>/delete', views.membership_delete, name='membership_delete'),
	

	


    path('class/', views.class_list, name='class_list'),
    # #URL타고 왔으니 여기서 TEMPLATE로 보내줄꺼야.
    path('class/<int:pk>/' , views.class_detail, name='class_detail'),
    path('class/<int:pk>/modify' , views.class_modify, name='class_modify'),
    path('class/open/', views.class_open, name='class_open'),
    path('class/open/choice/', views.class_open_choice, name='class_open_choice'),
    path('class/<int:pk>/delete/', views.class_delete, name='class_delete'),
    path('class/<int:pk>/reserve', views.class_reserve, name='class_reserve'), #상세페이지 예약
    path('class/<int:pk>/ticket/create', views.class_ticket_create, name='class_ticket_create'), 
    path('class/<int:pk>/ticket/list', views.class_ticket_list, name='class_ticket_list'), 

    # #####리뷰
    # path('class/<int:pk>/review' , views.class_review, name='class_review' ),
    path('class/<int:pk>/riview/create/', views.class_review_create, name='class_review_create'),
    path('class/review/<int:pk>/delete',views.review_delete,name='review_delete'),
    path('class/review/<int:pk>/modify', views.review_modify, name='review_modify'),
    # # path('class/<int:pk>/category',views.class_category,name='class_category'),
    # path('class/<int:pk>/price',views.class_price,name='class_price'),
    # path('class/<int:pk>/info',views.class_info,name='class_info'),


############## 검색
    path('search/', views.search_view, name='search'),
]
