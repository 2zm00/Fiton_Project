from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from fiton.models import Class,Center,Instructor,Review
from django.db.models import Prefetch
# from fiton.models import Class,User,Instructor,Review

#--- TemplateView
#기본 홈페이지를 렌더링하는 뷰
#template_name = 'home.html' 홈.html을 반환한다
class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 랜덤 강사 및 리뷰 로직 (기존 로직 유지)
        random_instructors = Instructor.objects.order_by('?')[:4]
        instructor_reviews = {}
        for instructor in random_instructors:
            classes = instructor.classes.all()  # 강사의 모든 수업
            reviews = Review.objects.filter(
                class_reviewed__in=classes
            ).select_related('member', 'class_reviewed')
            instructor_reviews[instructor] = reviews

        # 추가: "요가" 클래스 전체 가져오기
        yoga_classes = Class.objects.filter(
            exercise__name="요가",  
            is_deleted=False
        ).order_by('?')[:5]
        health_classes = Class.objects.filter(
            exercise__name="헬스",  
            is_deleted=False
        ).order_by('?')[:5]
        pilates_classes = Class.objects.filter(
            exercise__name="필라테스",  
            is_deleted=False
        ).order_by('?')[:5]

        context['stars'] = range(1, 6)
        context['random_classes'] = Class.objects.order_by('?')[:5]  # 기존 랜덤 클래스
        context['random_instructors'] = random_instructors
        context['instructor_reviews'] = instructor_reviews
        context['yoga_classes'] = yoga_classes 
        context['health_classes'] = health_classes  
        context['pilates_classes'] = pilates_classes  

        return context



class UserCreateView(generic.CreateView):
    template_name='registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('signup_done')

class UserCreateDoneTV(generic.TemplateView):
    template_name='registration/signup_done.html'