from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json
from .forms import (
    CustomUserCreationForm,CustomUserChangeForm, MemberForm,CenterOwnerForm, CenterForm, InstructorForm, 
    InstructorApplicationForm, ClassForm, ClassTicketForm, 
    ClassTicketOwnerForm, ReservationForm, ReviewForm, 
    MembershipForm, MembershipOwnerForm
)
from .models import (
    User, Member, CenterOwner, Exercise, Center, Instructor, InstructorApplication,
    Class, ClassTicket, ClassTicketOwner, Reservation, Review, Membership, MembershipOwner
)
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

############################## 로그인 및 인증
def signup(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()  # 사용자 생성
            role = user_form.cleaned_data.get('role')
            

            # 역할에 따른 폼 유효성 검사 및 저장
            if role == 'member':
                member_form = MemberForm(request.POST)
                if member_form.is_valid():
                    member = member_form.save(commit=False)
                    member.user = user
                    member.save()

            elif role == 'instructor':
                instructor_form = InstructorForm(request.POST)
                if instructor_form.is_valid():
                    instructor = instructor_form.save(commit=False)
                    instructor.user = user
                    instructor.save()

            elif role == 'centerowner':
                centerowner_form = CenterOwnerForm(request.POST)
                if centerowner_form.is_valid():
                    print(f"Role selected: {role}")
                    centerowner = centerowner_form.save(commit=False)
                    centerowner.user = user
                    centerowner.save()
            else:
                print(f"Unknown role: {role}")
        return redirect('home')
    
    else:
        user_form = CustomUserCreationForm()
        context = {
            'user_form': user_form,
        }
    return render(request, 'registration/signup.html', context=context)


def signup_choice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        role = data.get('role')
        # 역할에 따라 폼 렌더링
        if role == "member":
            rendered_form = render_to_string('registration/signup_choice.html', {'form': MemberForm()})
        elif role == "instructor":
            rendered_form = render_to_string('registration/signup_choice.html', {'form': InstructorForm()})
        elif role == "centerowner":
            rendered_form = render_to_string('registration/signup_choice.html', {'form': CenterOwnerForm()})
        return JsonResponse({"rendered_form": rendered_form})

      

def signup_done(request):
    return render(request, 'registration/signup_done.html')

def signup_delete(request):
    return render(request, 'registration/signup_delete.html')


############################## 프로필
def profile_user(request,user_id):
    user = User.objects.get(id=user_id)
    context={
        'user':user
    }
    return render(request, 'fiton/profile_user.html', context=context)



def profile_modify(request,user_id):
    user = User.objects.get(id=user_id)
    role = user.role
    user_form=CustomUserChangeForm(instance=user)
    # 역할에 따라 다른 폼 제공
    if role == 'member':
        ProfileForm = MemberForm
        instance=Member.objects.get(user_id=user_id)
    elif role == 'instructor':
        ProfileForm = InstructorForm
        instance=Instructor.objects.get(user_id=user_id)

    elif role == 'centerowner':
        ProfileForm = CenterOwnerForm()
        instance=CenterOwner.objects.get(user_id=user_id)

    else:
        return redirect('home')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=instance)
        user_form=CustomUserChangeForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid() and user_form.is_valid():
            user=user_form.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('fiton:profile_user', user_id=user.id)
    else:
        form = ProfileForm(instance=instance)
    context={
        'form': form,
        'role': role,
        'user_form':user_form
    }
    return render(request, 'fiton/profile_modify.html', context=context)











############################## 강사
def instructor_list(request):
    users=User.objects.filter(role='instructor')
    context={
        'users':users
    }
    return render(request,"fiton/instructor_list.html",context=context)



def instructor_detail(request,user_id):
    user=User.objects.get(id=user_id)
    context={
        'user':user
    }
    return render(request,"fiton/instructor_detail.html",context=context)



############################## 센터
def center(request):
    center_list = Center.objects.all()
    context = {'center_list': center_list}
    return render(request, 'fiton/center.html', context)

def center_detail(request, pk):
    center = Center.objects.prefetch_related('exercise').get(pk=pk)
    context = {'center': center}
    return render(request, 'fiton/center_detail.html', context)

@login_required
def center_register(request, pk):
    center = get_object_or_404(Center, pk=pk)

    return render(request, 'fiton/center_register.html', {'center': center})
@login_required
def center_register_button(request,pk):
    print("뷰 함수 진입")
    if request.user.role != 'instructor':
        messages.warning(request, "강사가 아닙니다.")
        return redirect('home')

    instructor = get_object_or_404(Instructor, user_id=request.user.pk)
    center = get_object_or_404(Center, pk=pk)

    duplicate_application = InstructorApplication.objects.filter(
        instructor=instructor, center=center
    ).first()
    if duplicate_application:
        messages.warning(request, "이미 신청한 센터입니다.")
    else:
        InstructorApplication.objects.create(
            instructor=instructor,
            center=center,
            status='pending'
        )
        messages.success(request, "센터 등록 신청이 완료되었습니다.")

    return redirect('fiton:center_detail', pk=center.pk)

def center_register_update(request, pk, status):
    application = get_object_or_404(InstructorApplication, pk=pk)
    if application.status == 'pending':
        application.status = status
        application.save()
        if application.status == 'approved':
            application.instructor.center.add(application.center)
            application.delete()
            
        else:
            application.delete()
            

    return redirect('fiton:center_register',application.center_id)



@login_required
def center_register_delete(request, pk,instructor_id):
    center = get_object_or_404(Center, pk=pk)
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    
    # 해당 강사가 수업을 개설했는지 확인
    if Class.objects.filter(instructor=instructor, center=center, is_deleted=False).exists():
        messages.error(request, '개설된 수업이 있는 강사는 센터 등록을 해지할 수 없습니다.')
        return redirect('fiton:center_detail', pk=pk)
    
    # 센터에서 강사 제거
    instructor.center.remove(center)
    messages.success(request, '센터 등록이 해지되었습니다.')

    
    return redirect('fiton:center_register',center.pk) 