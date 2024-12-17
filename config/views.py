from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


#--- TemplateView
#기본 홈페이지를 렌더링하는 뷰
#template_name = 'home.html' 홈.html을 반환한다
class HomeView(generic.TemplateView):
    template_name = 'home.html'


class UserCreateView(generic.CreateView):
    template_name='registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('signup_done')

class UserCreateDoneTV(generic.TemplateView):
    template_name='registration/signup_done.html'