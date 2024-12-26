from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json
from django.db.models import Avg
from django.utils import timezone 
from .forms import (
    CustomUserCreationForm,CustomUserChangeForm, MemberForm,CenterOwnerForm, CenterForm, InstructorForm, 
    InstructorApplicationForm, ClassForm, ClassTicketForm, 
    ClassTicketOwnerForm, ReservationForm, ReviewForm, 
    MembershipForm, MembershipOwnerForm
)
from .models import (
    User, Member, CenterOwner, Exercise, Center, Instructor, InstructorApplication,Notification,
    Class, ClassTicket, ClassTicketOwner,Class_type, Reservation, Review, Membership, MembershipOwner
)
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from django.core.cache import cache

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
        return redirect('fiton:signup_done')
    
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
    user=User.objects.get(pk=request.user.id)
    user.delete()
    return render(request, 'registration/signup_delete.html')
############################## 알림
@login_required
def notification_list(request):
    # 현재 사용자에게 전달된 알림만 가져오기
    notifications = request.user.notifications.all().order_by('-created_at')

    return render(request, 'fiton/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, pk):

    # 특정 알림을 읽음 처리
    notification = Notification.objects.filter(pk=pk, user=request.user).first()
    if notification:
        notification.is_read = True
        notification.save()

    return redirect('fiton:notification_list')

############################## 프로필
@login_required
def profile_user(request,user_id):
    user = User.objects.get(id=user_id)
    context={
        'user':user
    }
    return render(request, 'fiton/profile_user.html', context=context)
@login_required
def myclass_list(request,user_id):
    member = request.user.member
    reservations = Reservation.objects.filter(member=member).select_related('class_reserved')
    
    for reservation in reservations:
        time_remaining = reservation.class_reserved.start_class - timezone.now()
        days_remaining = time_remaining.days
        if days_remaining <=0:
            reservation.status='class start'
            reservation.save()
        
    return render(request, 'fiton/myclass_list.html', {
        'reservations': reservations,
        'days_remaining':days_remaining,
    })



@login_required
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
    instructor = get_object_or_404(Instructor, id=user.instructor.id)
    classes = instructor.classes.all()
    reviews = Review.objects.filter(class_reviewed__in=classes).select_related('member', 'class_reviewed')
    context={
        'user':user,
        'classes': classes,
        'reviews': reviews,

    }
    return render(request,"fiton/instructor_detail.html",context=context)



############################## 센터
def center(request):
    center_list = Center.objects.all()
    context = {'center_list': center_list}
    return render(request, 'fiton/center.html', context)

def center_detail(request, pk):
    center = Center.objects.prefetch_related('exercise').get(pk=pk)
    if request.user.role == 'instructor':

        exists=request.user.instructor.center.filter(id=center.id).exists()
        context = {'center': center,'exists':exists}
    else:
        context = {'center': center}

    return render(request, 'fiton/center_detail.html', context)

@login_required
def center_register(request, pk):
    center = get_object_or_404(Center, pk=pk)

    return render(request, 'fiton/center_register.html', {'center': center})
@login_required
def center_register_button(request,pk):
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


###############수업
@login_required
def class_open(request):
    
    if request.method == 'POST':
        form = ClassForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClassForm(user=request.user)
    return render(request, 'fiton/class_open.html', {'form': form})

@login_required
def class_open_choice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        center_id = data.get('center')
        if center_id:
            instructors = Instructor.objects.filter(center__id=center_id).values('id', 'user__name')
            
            return JsonResponse({'instructors': list(instructors)})

def class_list(request): #수업리스트 페이지
    # 전체 삭제되지 않은 수업 가져오기
    classes = Class.objects.filter(is_deleted=False)
    context = {'classes': classes}
    return render(request, 'fiton/class_list.html', context)


def class_detail(request, pk): 
    #수업의 (번호=pk) 를 담는 정보를 가져와야한다 = pk
    #MODEL
    classes = Class.objects.select_related('center', 'instructor').get(pk=pk)
    
    if request.method=='GET':
        reviews=Review.objects.filter(class_reviewed_id=pk)
        form = ReviewForm()
        context = {
            'classes': classes,
            'reviews':reviews,
            'form':form,
        }
        return render(request, 'fiton/class_detail.html', context)
    else:
        form=ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.member = Member.objects.get(user=request.user)  # 현재 사용자와 연결된 Member 설정
            review.class_reviewed = classes
            review.save()
            return redirect('fiton:class_detail',pk=pk)
@login_required
def class_modify(request,pk):
    classes = Class.objects.get(pk=pk)
    if request.method == 'GET':
        form = ClassForm(instance=classes,user=request.user,center=classes.center)
        context={'form':form}
        return render(request, 'fiton/class_modify.html', context )
    else:
        form = ClassForm(request.POST, instance=classes)
        if form.is_valid():
            form.save() 
            
            return redirect('fiton:class_detail', pk=pk)
        else:
            # 폼 검증 실패 시 템플릿 다시 렌더링
            context = {'form': form}
            return render(request, 'fiton/class_modify.html', context)
@login_required
def class_delete(request, pk):
    classes = get_object_or_404(Class, pk=pk)
    reservations = Reservation.objects.filter(class_reserved=classes)
    for reservation in reservations:
        reservation.status = 'class canceled'
        reservation.save()
    classes.delete()

    return redirect('home')

@login_required
def class_ticket_create(request, pk):
    classes=Class.objects.get(pk=pk)
    if request.method == 'POST':
        form=ClassTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fiton:class_detail',pk=pk)
    else:
        form=ClassTicketForm(pk=pk)
    return render(request,'fiton/class_ticket_create.html',context={'form':form})
    
def class_ticket_list(request,pk):
    classes=Class.objects.get(pk=pk)
    class_ticket=ClassTicket.objects.filter(class_type_id=classes.class_type.id)
    return render(request,'fiton/class_ticket_list.html',context={'class_ticket':class_ticket})


@login_required
def class_reserve(request, pk):
    # 예약할 클래스 가져오기
    classes = get_object_or_404(Class, pk=pk)

    if request.method == 'POST':
        try:
            # 현재 로그인된 멤버 확인
            member = request.user.member

            # 현재 클래스에 예약된 멤버 수 (status='reserved'인 경우만)
            reserved_count = Reservation.objects.filter(
                class_reserved=classes,
                status='reserved'
            ).count()

            # 예약 상태 결정
            if reserved_count < classes.max_member:
                # 정원이 초과되지 않았을 때 예약 확정
                status = 'reserved'
                messages.success(request, '예약이 성공적으로 완료되었습니다.')
            else:
                # 정원이 초과되었을 때 예약 대기
                status = 'Waiting for the reservation'
                messages.info(request, '정원이 초과되어 대기 상태로 예약되었습니다.')

            # 예약 생성
            reservation = Reservation.objects.create(
                member=member,
                class_reserved=classes,
                status=status,
            )
            reservation.save()

        except Exception as e:
            # 에러 처리
            messages.error(request, f'예약 처리 중 문제가 발생했습니다: {str(e)}')

        return redirect('fiton:myclass_list',pk=member.id)  # 적절한 페이지로 리다이렉트

    # GET 요청은 리다이렉트
    return redirect('home')
@login_required
def cancel_reservation(request, pk):
    # 취소할 예약 가져오기
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        try:
            # 예약 취소 처리
            reservation.status = 'reservation canceled'
            reservation.canceled_at = timezone.now()
            reservation.save()

            # 대기 중인 첫 번째 멤버를 reserved로 변경
            waiting_reservation = Reservation.objects.filter(
                class_reserved=reservation.class_reserved,
                status='Waiting for the reservation'
            ).order_by('reserved_at').first()

            if waiting_reservation:
                waiting_reservation.status = 'reserved'
                waiting_reservation.save()

            messages.success(request, '예약이 취소되었습니다')

        except Exception as e:
            # 에러 처리
            messages.error(request, f'예약 취소 처리 중 문제가 발생했습니다: {str(e)}')

        return redirect('fiton:myclass_list',pk=request.user.member.id)  # 적절한 페이지로 리다이렉트

    # GET 요청은 리다이렉트
    return redirect('home')



@login_required
def class_review_create(request, pk):
    classes = get_object_or_404(Class, pk=pk)
    member=get_object_or_404(Member,pk=request.user.member.id)
    instructor = classes.instructor
    if Review.objects.filter(member=member, class_reviewed=classes).exists():
        member = request.user.member
        reservations = Reservation.objects.filter(member=member).select_related('class_reserved')
        return render(request, 'fiton/myclass_list.html', {'message': '이미 리뷰를 작성하셨습니다.','reservations':reservations})
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review=form.save(commit=False)
            review.member=member
            review.class_reviewed=classes
            review.save()

            class_obj = instructor.classes.all()  # 강사의 모든 수업
            reviews = Review.objects.filter(class_reviewed__in=class_obj)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
            average_rating = round(average_rating, 1)
            instructor.average_rating = average_rating
            instructor.save()
            
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'fiton/class_review_create.html', {'form': form})
    
@login_required
def review_delete(requset,pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('fiton:class_detail',review.class_reviewed.id)
@login_required
def review_modify(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'fiton/review_modify.html', context={'form': form})  # 'return' 추가
    else:
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('fiton:class_detail', pk=review.class_reviewed.id)
        else:
            return render(request, 'fiton/review_modify.html', context={'form': form})  # 'return' 추가


@login_required
def center_create(request):
    center_owner = get_object_or_404(CenterOwner, user=request.user)

    if request.method == 'POST':
        form = CenterForm(request.POST)
        if form.is_valid():
            center = form.save(commit=False)
            center.owner = center_owner 
            center.save()
            return redirect('fiton:center_detail', pk=center.pk)
    else:
        form = CenterForm()
    
    context = {
        'form': form,
        'center_owner': center_owner
    }

    return render(request, 'fiton/center_create.html', context)



############################## 멤버쉽(회원권)

#멤버쉽 리스트(회원도 멤버쉽 사야하고, 센터장도 센터에서 멤버쉽 발급해야하니까.)
def membership_list(request, pk):
    center = get_object_or_404(Center, pk=pk)
    membership_list = Membership.objects.filter(center=center)
    
    context = {
        'center': center,
        'membership_list': membership_list,
    }
    return render(request, 'fiton/membership_list.html', context)


######## 결제 로직만들때 회원권 구매 다시 살펴보아야함.
#회원권 구매 페이지 
@login_required
def membership_purchase(request, center_pk, membership_pk):
    center = get_object_or_404(Center, pk=center_pk)  
    membership = get_object_or_404(Membership, pk=membership_pk)

    if request.method == 'POST':
        # 구매 처리 로직
        return redirect('fiton:membership_purchase_done', pk=membership.pk)
    
    context = {
        'center': center,
        'membership': membership,
    }
    return render(request, 'fiton/membership_purchase.html', context)

#회원권 구매 성공 페이지
def membership_purchase_done(request, center_pk, membership_pk):
    center = get_object_or_404(Center, pk=center_pk)  
    membership = get_object_or_404(Membership, pk=membership_pk)
    context = {
        'center': center,
        'membership': membership,
    }
    return render(request, 'fiton/membership_purchase_done.html', context)

#회원권 발급 페이지
@login_required
def membership_create(request, pk):
    center = get_object_or_404(Center, pk=pk)  

    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.center = center
            membership.user = request.user  # user 자동 할당
            membership.save()
            return redirect('fiton:membership_list', pk=center.pk)
    else:
        form = MembershipForm()

    context = {
        'center': center,
        'form': form,
    }
    return render(request, 'fiton/membership_create.html', context)

#멤버쉽 상세페이지 /membership/<int:pk>
@login_required
def membership_detail(request, center_pk, membership_pk):
    center = get_object_or_404(Center, pk=center_pk)
    membership = get_object_or_404(Membership, pk=membership_pk)
    context = {
        'center': center, 
        'membership' : membership,
    }
    return render(request, 'fiton/membership_detail.html', context)

#멤버쉽 수정 /membership/<int:pk>/modify

@login_required
def membership_modify(request, center_pk, membership_pk):
    center = get_object_or_404(Center, pk=center_pk)
    membership = get_object_or_404(Membership, pk=membership_pk)
    
    # 센터 소유자 권한 확인
    if request.user != center.owner.user:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('fiton:membership_detail', center_pk=center_pk, membership_pk=membership_pk)
    
    if request.method == 'POST':
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            membership = form.save(commit=False)
            membership.center = center
            membership.save()
            return redirect('fiton:membership_detail', center_pk=center_pk, membership_pk=membership_pk)
    else:
        form = MembershipForm(instance=membership)
    
    context = {
        'center': center,
        'membership': membership,
        'form': form,
    }
    return render(request, 'fiton/membership_modify.html', context)

#멤버쉽 삭제 /membership/<int:pk>/delete
@login_required
def membership_delete(request, center_pk, membership_pk):
    center = get_object_or_404(Center, pk=center_pk)
    membership = get_object_or_404(Membership, pk=membership_pk)
    
    # 센터 소유자 권한 확인
    if request.user != center.owner.user:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('fiton:membership_detail', center_pk=center_pk, membership_pk=membership_pk)
    
    if request.method == 'POST':
        membership.delete()
        return redirect('fiton:membership_list', pk=center_pk) 
    
    context = {
        'center': center,
        'membership': membership,
    }
    return render(request, 'fiton/membership_delete.html', context)




############################## 검색기능

def search_view(request):
    query = request.GET.get('q', '')
    exercise_filter = request.GET.get('exercise', '')
    
    try:
        cache_key = f'search_results_{query}_{exercise_filter}'
        results = cache.get(cache_key)
        
        if results is None:
            centers = Center.objects.select_related('owner').prefetch_related(
                'exercise', 
                'instructors'
            )
            
            if query:
                centers = centers.filter(
                    Q(name__icontains=query) |
                    Q(location__icontains=query) |
                    Q(exercise__name__icontains=query) |
                    Q(instructors__user__name__icontains=query)
                ).distinct()
            
            if exercise_filter:
                centers = centers.filter(exercise__name=exercise_filter)
            
            cache.set(cache_key, centers, 300)
            results = centers

        # AJAX 요청인 경우 JSON 응답
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = [{
                'id': center.id,
                'name': center.name,
                'location': center.location,
                'exercises': [ex.name for ex in center.exercise.all()],
                'instructors': [inst.user.name for inst in center.instructors.all()]
            } for center in results]
            return JsonResponse({'results': data})
            
        # 일반 요청인 경우 템플릿 렌더링
        exercises = Exercise.objects.all()
        context = {
            'results': results,
            'query': query,
            'exercises': exercises,
            'selected_exercise': exercise_filter
        }
        return render(request, 'fiton/search/search.html', context)
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        return render(request, 'fiton/search/search.html', {
            'error': str(e),
            'query': query
        })