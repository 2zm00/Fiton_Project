from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from fiton.models import Class,Center,Instructor,Review
from django.db.models import Prefetch
from config.settings import OPENAI_API_KEY
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import re
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db.models import Count
#--- TemplateView
#기본 홈페이지를 렌더링하는 뷰
#template_name = 'home.html' 홈.html을 반환한다
class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 캐시 키 설정
        cache_key = "popular_instructor"
        cache_expiry_key = "popular_instructor_last_updated"

        # 캐시에서 데이터 가져오기
        popular_instructor = cache.get(cache_key)
        last_updated = cache.get(cache_expiry_key)

        # 캐시가 없거나, 캐시된 데이터가 한 달 이상 된 경우 새로 계산
        if not popular_instructor or not last_updated or last_updated < datetime.now() - timedelta(days=30):
            # 랭체인 작업 수행
            pg_uri = f"postgresql+psycopg2://{os.getenv('db_user')}:{os.getenv('db_pwd')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"

            db = SQLDatabase.from_uri(pg_uri)
            db.get_usable_table_names()
            llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0) # gpt-4-turbo
            chain = create_sql_query_chain(llm, db)
            execute_query = QuerySQLDataBaseTool(db=db)
            write_query = create_sql_query_chain(llm, db)
            chain = write_query | execute_query
            answer_prompt = PromptTemplate.from_template(
                """주어진 유저 질문에 대해서, corresponding SQL query, and SQL result, answer the user question.
                Question: {question}
                SQL Query: {query}
                SQL Result: {result}
                Answer: """
                )
            parser = StrOutputParser()
            answer = answer_prompt | llm | parser
            chain = (
                RunnablePassthrough.assign(query=write_query).assign(
                    result=itemgetter("query") | execute_query
                )
                | answer
            )

            # 질문 실행
            response=chain.invoke({"question": "이번달에 시작한 수업들중에서 예약의 상태가 Class Completed인 멤버들의 합이 가장많은 수업의 강사의 id는?? "},) # RAG 연결 모델

            response = chain.invoke({
                "question": "이번달에 시작한 수업들을 강사별로 묶은다음에 묶인 수업들의 예약의 상태가 Class Completed인 예약이 제일 많은 강사의 id와 예약 수는?"
            })

            # 결과에서 강사 ID 추출
            match = re.search(r"id는 (\d+)", response)
            if match:
                instructor_id = int(match.group(1))
                popular_instructor = Instructor.objects.get(id=instructor_id)

                # 캐시에 결과 저장
                cache.set(cache_key, popular_instructor, timeout=2592000)  # 30일 (초 단위)
                cache.set(cache_expiry_key, datetime.now(), timeout=2592000)
            else:
                print("강사 ID를 찾을 수 없습니다.")
                popular_instructor = None

        # 캐시에 저장된 인기 강사를 컨텍스트에 추가
        context['popular_instructor'] = popular_instructor

        # 기타 데이터 설정
        random_instructors = Instructor.objects.order_by('?')[:4]
        instructor_reviews = {}
        for instructor in random_instructors:
            classes = instructor.classes.all()
            reviews = Review.objects.filter(
                class_reviewed__in=classes
            ).select_related('member', 'class_reviewed')
            instructor_reviews[instructor] = reviews

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
        context['random_classes'] = Class.objects.order_by('?')[:5]
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