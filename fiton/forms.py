from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import get_object_or_404
from .models import (
    User, Member, CenterOwner, Exercise, Center, Instructor, InstructorApplication,Amenity,
    Class, ClassTicket, ClassTicketOwner, Reservation, Review, Membership, MembershipOwner,Class_type
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 비밀번호 필드를 비활성화하거나 삭제
        if 'password' in self.fields:
            del self.fields['password']

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
    exercise = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '운동 종목을 쉼표로 구분하여 입력하세요. (예: 요가, 필라테스, 헬스)',
            'rows': 3,
        }),
        label="운동 종목",
        required=True,
    )
    amenity = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '편의 시설을 쉼표로 구분하여 입력하세요. (예: 주차장, 휴게실, 락커룸, 샤워실)',
            'rows': 3,
        }),
        label="편의 시설",
        required=False,
    )

    class Meta:
        model = Center
        fields = ['name', 'location', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '센터 이름'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '센터 위치'
            }),
            'image':forms.FileInput(
                attrs={'class':'form-control',}
            ),
        }
        labels = {
            'name': '센터 이름',
            'location': '센터 위치',
        }

    def __init__(self, *args, **kwargs):
        # 사용자 정보를 추가로 받기 위한 인수
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        운동 종목을 저장할 때 자동으로 Exercise 모델에 추가하고
        로그인한 사용자를 소유자로 설정
        """
        # Center 객체 생성
        center = super().save(commit=False)

        # 현재 로그인한 사용자를 owner로 설정
        if self.user and hasattr(self.user, 'centerowner'):
            center.owner = self.user.centerowner
        else:
            raise ValueError("센터 소유자(centerowner)만 센터를 등록할 수 있습니다.")

        # Center 객체 저장
        if not center.pk:
            center.save()

        # 운동 종목 처리
        exercises = self.cleaned_data.get('exercise', '')
        if exercises:
            exercise_list = [e.strip() for e in exercises.split(',') if e.strip()]
            exercise_objs = [Exercise.objects.get_or_create(name=exercise_name)[0] for exercise_name in exercise_list]
            center.exercise.add(*exercise_objs)

        amenities = self.cleaned_data.get('amenity', '')
        if amenities:
            amenity_list = [e.strip() for e in amenities.split(',') if e.strip()]
            amenity_objs = [Amenity.objects.get_or_create(name=amenity_name)[0] for amenity_name in amenity_list]
            center.amenity.add(*amenity_objs)

        # 최종 저장
        if commit:
            center.save()


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
    class_type = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '수업권 종류를 입력하세요. (수업권을 구분짓는 항목입니다.)'
        }),
        label="수업권 종류"
    )
    class Meta:
        model = Class
        fields = ['name', 'center', 'instructor','exercise', 'content', 'location', 'start_class', 'reservation_permission', 'cancellation_permission', 'max_member', 'min_memeber']
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
            'exercise': forms.Select(attrs={
                'class': 'form-control',
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '수업 내용을 입력하세요'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '센터 내 수업 장소'
            }),
            'start_class': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'reservation_permission': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'cancellation_permission': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
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
    def __init__(self, *args, user=None,center=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            if user.role == 'instructor':
                instructor = get_object_or_404(Instructor, user_id=user.id)
                self.fields['instructor'].initial = instructor.id
                self.fields['instructor'].queryset = Instructor.objects.filter(id=instructor.id)
                if center:
                    self.fields['center'].queryset = Center.objects.filter(id=center.id)
                else:
                    self.fields['center'].queryset = instructor.center.all()
                
                
            elif user.role == 'centerowner':
                centerowner = CenterOwner.objects.get(user_id=user.id)
                self.fields['center'].queryset = Center.objects.filter(owner_id=centerowner.id)
    def save(self):
    # 폼 데이터 저장 전 처리
        instance = super().save(commit=False)

        # class_type 설정
        class_type_name = self.cleaned_data['class_type']
        class_type, created = Class_type.objects.get_or_create(name=class_type_name)

        instance.class_type = class_type

        # 바로 저장
        instance.save()
        return instance

       
    
   

class ClassTicketForm(forms.ModelForm):
    class Meta:
        model = ClassTicket
        fields = ['class_type', 'price','ticket_quantity']
        widgets = {
            'class_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '가격'
            }),
            'ticket_quantity': forms.NumberInput(attrs={  
                'class': 'form-control',
                'placeholder': '수업권 횟수'
            }),
        }
    def __init__(self, *args, pk=None ,**kwargs):
        super().__init__(*args, **kwargs)

        if pk:
            classes = get_object_or_404(Class, pk=pk)
            self.fields['class_type'].initial = classes.class_type.name
            self.fields['class_type'].queryset = Class_type.objects.filter(name=classes.class_type.name)
            
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
        fields = ['rating', 'comment']
        widgets = {
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
        fields = ['name', 'price', 'duration'] 
        widgets = {
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
                'placeholder': '기간(일)'
            })
        }


class MembershipOwnerForm(forms.ModelForm):
    class Meta:
        model = MembershipOwner
        fields = ['member', 'center', 'end_date', 'is_active']
        widgets = {
            'member': forms.Select(attrs={
                'class': 'form-control',
            }),
            'center': forms.Select(attrs={
                'class': 'form-control',
            }),
            
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

