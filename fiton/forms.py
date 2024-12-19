from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import get_object_or_404
from .models import (
    User, Member, CenterOwner, Exercise, Center, Instructor, InstructorApplication,
    Class, ClassTicket, ClassTicketOwner, Reservation, Review, Membership, MembershipOwner
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','role', 'name', 'gender','phone_number','image', 'date_of_birth',)
        widgets ={
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'ID입력'

            })
        }
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','role', 'name', 'gender','phone_number','image', 'date_of_birth',)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['height', 'weight', 'goal_weight', 'body_fat', 'skeletal_muscle', 'health_info']
        widgets = {
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '키 (cm)'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '체중 (kg)'
            }),
            'goal_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '목표 체중 (kg)'
            }),
            'body_fat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '체지방률 (%)'
            }),
            'skeletal_muscle': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '골격근량 (kg)'
            }),
            'health_info': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '건강 정보를 입력하세요'
            }),
            
        }

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ['name', 'location', 'owner', 'exercise']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '센터 이름'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '센터 위치'
            }),
            'owner': forms.Select(attrs={
                'class': 'form-control',
            }),
            'exercise': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }

class CenterOwnerForm(forms.ModelForm):
    class Meta:
        model = CenterOwner
        fields = ['business_registration_number']
        widgets = {
            'business_registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '사업자 번호'
            }),
        }


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [ 'expertise', 'available_hours', 'introduction', 'certification', 'career']
        widgets = {
            'expertise': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '전문 분야'
            }),
            'available_hours': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '수업 가능 시간'
            }),
            'introduction': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '자기소개'
            }),
            'certification': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '자격증 정보'
            }),
            'career': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '경력'
            }),
        }

class InstructorApplicationForm(forms.ModelForm):
    class Meta:
        model = InstructorApplication
        fields = ['instructor', 'center', 'status']
        widgets = {
            'instructor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'center': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'center', 'instructor', 'class_type', 'content', 'location', 'start_class', 'reservation_permission', 'cancellation_permission', 'max_member', 'min_memeber']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '수업 이름'
            }),
            'center': forms.Select(attrs={
                'class': 'form-control',
            }),
            'instructor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'class_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '수업 종류'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '수업 내용을 입력하세요'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '수업 장소'
            }),
            'start_class': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }),
            'reservation_permission': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }),
            'cancellation_permission': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM:SS'
            }),
            'max_member': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '최대 인원'
            }),
            'min_memeber': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '최소 인원'
            }),
        }
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            if user.role == 'instructor':
                instructor = get_object_or_404(Instructor, user_id=user.id)
                self.fields['instructor'].initial = instructor.id
                self.fields['instructor'].queryset = Instructor.objects.filter(id=instructor.id)
                self.fields['center'].queryset = instructor.center.all()
            elif user.role == 'centerowner':
                centerowner = CenterOwner.objects.get(user_id=user.id)
                self.fields['center'].queryset = Center.objects.filter(owner_id=centerowner.id)
               

       
    
   

class ClassTicketForm(forms.ModelForm):
    class Meta:
        model = ClassTicket
        fields = ['class_name', 'price']
        widgets = {
            'class_name': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '가격'
            }),
        }

class ClassTicketOwnerForm(forms.ModelForm):
    class Meta:
        model = ClassTicketOwner
        fields = ['member', 'class_ticket', 'quantity']
        widgets = {
            'member': forms.Select(attrs={
                'class': 'form-control',
            }),
            'class_ticket': forms.Select(attrs={
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '수업권 개수'
            }),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['member', 'class_reserved', 'status']
        widgets = {
            'member': forms.Select(attrs={
                'class': 'form-control',
            }),
            'class_reserved': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['member', 'class_reviewed', 'rating', 'comment']
        widgets = {
            'member': forms.Select(attrs={
                'class': 'form-control',
            }),
            'class_reviewed': forms.Select(attrs={
                'class': 'form-control',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '평점'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '리뷰 내용을 입력하세요'
            }),
        }

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['center', 'name', 'price', 'duration']
        widgets = {
            'center': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '회원권 이름'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '가격'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '기간 (일)'
            }),
        }

class MembershipOwnerForm(forms.ModelForm):
    class Meta:
        model = MembershipOwner
        fields = ['member', 'membership', 'end_date', 'is_active']
        widgets = {
            'member': forms.Select(attrs={
                'class': 'form-control',
            }),
            'membership': forms.Select(attrs={
                'class': 'form-control',
            }),
            
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

