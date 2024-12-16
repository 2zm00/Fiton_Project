from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Member, CenterOwner, Exercise, Center, Instructor, InstructorApplication,
    Class, ClassTicket, ClassTicketOwner, Reservation, Review, Membership, MembershipOwner
)


# 기본 User 모델 확장 등록
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'name', 'gender', 'phone_number', 'image', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'name', 'gender', 'phone_number', 'image', 'date_of_birth'),
        }),
    )

admin.site.register(User, CustomUserAdmin)

# 수강생, 센터장, 강사 관련 모델 등록
admin.site.register(Member)
admin.site.register(CenterOwner)
admin.site.register(Instructor)
admin.site.register(InstructorApplication)

# 운동 및 센터 관련 모델 등록
admin.site.register(Exercise)
admin.site.register(Center)

# 수업 및 수업권 관련 모델 등록
admin.site.register(Class)
admin.site.register(ClassTicket)
admin.site.register(ClassTicketOwner)

# 예약 및 리뷰 관련 모델 등록
admin.site.register(Reservation)
admin.site.register(Review)

# 회원권 관련 모델 등록
admin.site.register(Membership)
admin.site.register(MembershipOwner)
