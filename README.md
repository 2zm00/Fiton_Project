# Fit on - 피트니스 수업관리 시스템

📍 해당 프로젝트는 팀 프로젝트 작업물이며 재가공 및 재배포를 금하고 있습니다. 개인 정보가 포함되어 있어 레포지토리 포크를 원치 않습니다. 일부 소스 코드 참고 시 출처를 명시해주시면 감사하겠습니다.

## 프로젝트 소개

피트니스 산업의 지속적인 성장과 건강에 대한 관심 증가에 따라, 기존 PT 수업관리의 비효율적인 시스템을 개선하고자 Django 기반의 웹 서비스를 구현했습니다. 기존의 전화나 메시지로 이루어지던 수업 관리를 체계화하여 수강생, 강사, 센터 운영자 모두에게 효율적인 관리 시스템을 제공하고자 합니다.

## 해결하고자 하는 문제

**수강생 측면**
- 사적 채널을 통한 스케줄 조율의 비효율성
- 복잡한 예약/취소 프로세스
- 체계적인 수업 이용 내역 관리의 부재

**강사 측면**
- 수업 스케줄 관리의 어려움
- 개별 연락으로 인한 업무 부담
- 수업 노쇼 관리의 복잡성

**센터 운영 측면**
- 회원 정보의 체계적 관리 어려움
- 수기 기록으로 인한 정보 누락 위험
- 수업료 정산의 정확성 문제

## 프로젝트 개요

** 프로젝트 팀원**
- 2zm00 : 일정 관리, 인터페이스 구축, Git 관리, 관련 문서 작성, 기능 도입 
- mungwanwoo : 데이터베이스 관리, 프로젝트 기능 관리
- betkim : 프로젝트 기능 관리, QA 확인

**🎈 프로젝트 기간**
- 2024/12/11 ~ 2024/12/30

**✨ 핵심 기능**
- 결제 모듈 통합
- 디바운싱 기반 실시간 검색
- 이벤트 기반 알림 시스템
- 위치 기반 지도 서비스
- 사용자 인증 및 권한 관리
- 서비스 구매 및 판매 시스템
- 프로필 관리
- 선택적 공개 포스팅
- 리뷰 시스템
- 시간 기반 알림 서비스

## 기술 스택

**Backend**
- Django 5.1.3
- Python 3.11.10
- PostgreSQL

**Frontend**
- TailwindCSS
- HTML/CSS/JavaScript

**Infrastructure**
- PostgreSQL


## 구현 화면 및 핵심 기능

**메인 기능**
- 실시간 검색 및 지도 통합 인터페이스
- 강사 인증 및 수업 관리 시스템
- 회원권/수업권 구매 및 예약 시스템
- 센터 관리 및 회원권 생성
- 리뷰 시스템
- 자동화된 알림 시스템

## 추가 구현 예정

- [x] 결제 모듈 구현
- [x] 디바운싱 검색 기능
- [x] 이벤트 알림 시스템
- [x] 위치 정보 지도 기능
- [ ] AI 챗봇 서비스
- [ ] 실시간 채팅 시스템
- [ ] LangChain 기반 정보 검색
- [ ] 데이터 분석 대시보드

## 프로젝트 설치 및 실행

**1. 환경 설정**
```bash
# Miniconda 가상환경 생성
conda create -n fiton python=3.11
conda activate fiton
```

**2. 의존성 설치**
```bash
pip install -r requirements.txt
```

**3. 데이터베이스 설정**
```bash
python manage.py migrate
```

**4. 개발 서버 실행**
```bash
python manage.py runserver
```

## 폴더 구조
```
📦Fiton_Project
 ┣ 📂config
 ┃ ┣ 📂static
 ┃ ┃ ┣ 📜signup.js
 ┃ ┃ ┗ 📜style.css
 ┃ ┣ 📂templates
 ┃ ┃ ┣ 📂registration
 ┃ ┃ ┣ 📜base.html
 ┃ ┃ ┗ 📜home.html
 ┣ 📂fiton
 ┃ ┣ 📂static
 ┃ ┃ ┗ 📂fiton
 ┃ ┃    ┣ 📂images
 ┃ ┃    ┗ 📂js
 ┃ ┣ 📂templates
 ┃ ┃ ┗ 📂fiton
 ┃ ┃    ┗ 📂search
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜forms.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜signals.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📂maps
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📂media
 ┃ ┣ 📂center_images
 ┃ ┗ 📂profile_images
 ┣ 📂payments
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂profile_images
```

## 주요 라이브러리
- Django==5.1.3
- django-allauth==65.3.0
- Pillow==11.0.0
- psycopg2-binary==2.9.10
- python-dotenv==1.0.1

## 프로젝트 관련 링크
- Github 레포지토리 : https://github.com/2zm00/Fiton_Project
- 기획안 : https://docs.google.com/spreadsheets/d/1z0MNgjmX_-icLs5omh3fUv9CrDgwp_VYDUaUMc3BOqk/edit?usp=sharing
![fiton.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/c69962b0-3951-485b-b10a-5bb29576bba8/70d91bcc-4417-4af6-b696-d812238d9e22/fiton.gif)
- 요구사항 정의서
![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c69962b0-3951-485b-b10a-5bb29576bba8/b64ec27f-3fcc-469f-9c4f-76ffef05bb8e/image.png)
- ERD : https://www.erdcloud.com/d/298fbiaFf2XZf4Etd
![fiton_project - public.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c69962b0-3951-485b-b10a-5bb29576bba8/2701393d-10e0-402d-a415-90cc0f41cfc8/fiton_project_-_public.png)
![이커머스 프로젝트.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/c69962b0-3951-485b-b10a-5bb29576bba8/a8f419ba-5c53-44db-b792-448213621f94/%EC%9D%B4%EC%BB%A4%EB%A8%B8%EC%8A%A4_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8.png)
- 프로젝트 링크
- 발표자료 PPT
- 시연 영상
