from django.shortcuts import render
from fiton.models import *
import requests
import os

# Create your views here.


# Geocoding 함수
def center_map(request):
    # 이름과 주소(location)만 전달
    kakao_api_key = os.getenv('KAKAO_API_KEY')
    centers = list(Center.objects.values('id','name', 'location'))
    return render(request, 'maps/center_map.html', {'centers': centers, 'kakao_api_key': kakao_api_key})
