from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json
from .forms import (
    CustomUserCreationForm, MemberForm,CenterOwnerForm, CenterForm, InstructorForm, 
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
def center_register_delete(request, pk):
    center = get_object_or_404(Center, pk=pk)
    instructor = get_object_or_404(Instructor, user=request.user)
    
    # 해당 강사가 수업을 개설했는지 확인
    if Class.objects.filter(instructor=instructor, center=center, is_deleted=False).exists():
        messages.error(request, '개설된 수업이 있는 강사는 센터 등록을 해지할 수 없습니다.')
        return redirect('center_detail', pk=pk)
    
    # 센터에서 강사 제거
    instructor.center.remove(center)
    messages.success(request, '센터 등록이 해지되었습니다.')
    
    return redirect('fiton:center') 





############################## 수업

def class_list(request): #수업리스트 페이지
    # 전체 삭제되지 않은 수업 가져오기
    classes = Class.objects.filter(is_deleted=False)
    context = {'classes': classes}
    return render(request, 'fiton/class_list.html', context)

#수업 개설 작성자는 강사(instructor) /
# 수업 개설할 때 필요한 정보는  누가 수업을 개설하는가(강사 instructor)


# 강사의 정보가 필요하고
# 수업 이름(Class 모델의 name) # 어떤 수업을 개설할것인가() / 수업이름은 무엇인가?()
# 어디 센터에서 수업을 진행할것인가() / 수업 시간은 언제인가() 등이 필요합니다.

def class_open(request):
    #필요한 정보
    instructor = get_object_or_404(Instructor, user=request.user)
    
    #보낼 정보
    if request.method == 'POST':

        #form에서 다 해버림
        form = ClassForm(request.POST)
        if form.is_valid():
            classes = form.save(commit=False)
            classes.instructor = instructor
            
            #보내기만 하면되요 = 데이터베이스에 저장하겠다
            classes.save()

            #저장다 했으니 원래있던자리로 보내주겠다
            return redirect('fiton:class_list')
    else:
        form = ClassForm(initial={'instructor':  instructor})
    
    context = {
        'form': form,
        'instructor':  instructor,
    }

    return render(request, 'fiton/class_open.html', context)





def class_modify(request):
    return render(request, 'fiton/class_modify.html')

def class_delete(request,pk):
    return render(request, 'fiton/class_delete.html')
    
# @login_required
def class_delete(request, pk):
    classes = get_object_or_404(Class, pk=pk)
    classes.is_deleted = True  # 소프트 삭제
    classes.save()
    return redirect(request,'class_list')



#View/Model/Template 연결매체가 URL
#1
def class_detail(request, pk): 
    #수업의 (번호=pk) 를 담는 정보를 가져와야한다 = pk
    #MODEL
    classes = Class.objects.select_related('center', 'instructor').get(pk=pk)
    #VIEW
    context = {'classes' : classes}
    #URL로 보내줄꺼야.
    return render(request, 'fiton/class_detail.html', context)

def class_reserve(request):
    return render(request, 'fiton/class_reserve.html')

#2
def class_review(request, pk):
    classes = Class.objects.select_related('center', 'instructor').get(pk=pk)
    reviews = Review.objects.select_related('member', 'class_reviewed').filter(class_reviewed=classes)
    context = {'classes': classes, 'reviews': reviews}
    return render(request, 'fiton/class_review.html', context)

#수업 리뷰 생성
def class_review_create(request):
    
    # + 데이터 전송하는 로직 

    #데이터 가져오는 코드
    classes = get_object_or_404(Class, pk=classes.pk)
    
    # 템플릿 파일 ~~~.html 안에 <form method="POST">
    #<button type="submit">
    # 사람들이 리뷰(템플릿 페이지)를 입력할때 리뷰내용이 "아 이 영화 재밌었어요" <<이걸 보내줘야함 데이터베이스에

    #버튼을 누르면 <form method="POST">를 통해서 view 지금 아래 코드로 넘어와요
    #템플릿이 post를 통해서 views.py로 전달하고 여기로 왔을때 (if)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        #오류(빈칸이 있는지) 확인해주는 코드
        if form.is_valid():
            review = form.save(commit=False)
            #요청을 보낸 유저를 review의 author 작성자로 지정하겠다. 
            #author 는 models.py에서 정의했던 이름
            review.author = request.user #현재 로그인한 사용자를 리뷰
            #리뷰를 작성하는 film(오른쪽), 얘를 review에서 이 film(왼쪽)으로 하겠다. 
            review.class_reviewd = classes #리뷰가 속한 클래스 설정정
            #film을 정해주고, 작성자를 정해줬잖아요

            #저장을 하겠다
            review.save()

            #저장을 다 했으면 redirect 다시 이 페이지로 연결시켜주겠다. 
            #어디로? review-detail(url- name='review-detail') pk=review.pk
            #redirect하기 전 페이지가 review작성하는 페이지 -> review상세페이지
            return redirect('review-detail', pk=review.pk)
    #이거 요청이 POST가 아니면
    else:
        #다시 하겟다 initial (초기화  __init__ 초기화)
        form = ReviewForm(initial={'classes': classes})
    
    context= {'form': form, 'classes': classes,}
    # 저희가 model-view -- url -tenplate 보여줬으니
    # 사용자가 template(웹페이지)-POST통해서 보내고- url-view-> 위에 코드를 통해서 -model-> 데이터베이스에
    return render(request, 'fiton/class_review_create.html', context)



def class_review_delete(request):
    # + 데이터 삭제하는 로직
    return render(request, 'fiton/class_review_delete.html')

def class_review_modify(request):
    # + 데이터 수정하는 로직
    return render(request, 'fiton/class_review_modify.html')

def class_price(request):
    return render(request)

def class_info(request):
    pass