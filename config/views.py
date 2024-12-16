from django.views import generic




#--- TemplateView
#기본 홈페이지를 렌더링하는 뷰
#template_name = 'home.html' 홈.html을 반환한다
class HomeView(generic.TemplateView):
    template_name = 'base.html'