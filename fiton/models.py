from django.contrib.auth.models import AbstractUser
from django.db import models

# 기본 유저 모델 확장
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', '수강생'),
        ('instructor', '강사'),
        ('director', '센터장'),
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='student', 
        help_text="사용자의 역할", 
        verbose_name="역할"
    )
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        help_text="연락처", 
        verbose_name="전화번호"
    )
    address = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="주소", 
        verbose_name="주소"
    )
    image = models.ImageField(
        upload_to='profile_images/', 
        null=True, 
        blank=True, 
        help_text="프로필 이미지", 
        verbose_name="이미지"
    )

# 수강생 모델
class Student(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile', 
        verbose_name="사용자"
    )
    height = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="키 (cm)", 
        verbose_name="키"
    )
    weight = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="몸무게 (kg)", 
        verbose_name="몸무게"
    )
    goal_weight = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="목표 몸무게 (kg)", 
        verbose_name="목표 몸무게"
    )
    body_fat = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="체지방률 (%)", 
        verbose_name="체지방률"
    )
    skeletal_muscle = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="골격근량 (kg)", 
        verbose_name="골격근량"
    )
    health_info = models.TextField(
        null=True, 
        blank=True, 
        help_text="건강 정보", 
        verbose_name="건강 정보"
    )
    fit_time = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        help_text="운동 시간", 
        verbose_name="운동 시간"
    )

    def __str__(self):
        return f"{self.user.username} (수강생)"

# 강사 모델
class Instructor(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='instructor_profile', 
        verbose_name="사용자"
    )
    center = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text="소속 센터", 
        verbose_name="센터"
    )
    gender = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="성별", 
        verbose_name="성별"
    )
    city = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        help_text="도시", 
        verbose_name="도시"
    )
    district = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        help_text="구/군", 
        verbose_name="구/군"
    )
    expertise = models.CharField(
        max_length=255, 
        help_text="강의 가능 분야", 
        verbose_name="전문 분야"
    )
    certification = models.TextField(
        null=True, 
        blank=True, 
        help_text="자격증", 
        verbose_name="자격증"
    )
    career = models.TextField(
        null=True, 
        blank=True, 
        help_text="경력", 
        verbose_name="경력"
    )
    exercise = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text="주요 운동", 
        verbose_name="운동"
    )
    grade = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        help_text="등급", 
        verbose_name="등급"
    )
    time_available = models.TextField(
        null=True, 
        blank=True, 
        help_text="가능한 시간", 
        verbose_name="가능 시간"
    )
    account = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text="계좌 정보", 
        verbose_name="계좌"
    )

    def __str__(self):
        return f"{self.user.username} (강사)"

# 센터장 모델
class CenterDirector(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='director_profile', 
        verbose_name="사용자"
    )
    managed_centers = models.TextField(
        blank=True, 
        help_text="관리 중인 센터", 
        verbose_name="관리 센터"
    )
    center_location = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text="센터 위치", 
        verbose_name="센터 위치"
    )

    def __str__(self):
        return f"{self.user.username} (센터장)"

# 센터 모델
class Center(models.Model):
    name = models.CharField(
        max_length=255, 
        help_text="센터 이름", 
        verbose_name="센터 이름"
    )
    location = models.CharField(
        max_length=255, 
        help_text="센터 위치", 
        verbose_name="센터 위치"
    )
    owner = models.ForeignKey(
        CenterDirector, 
        on_delete=models.CASCADE, 
        related_name='owned_centers', 
        verbose_name="센터장"
    )

    def __str__(self):
        return f"{self.name} ({self.location})"

# 수업 모델
class Class(models.Model):
    title = models.CharField(
        max_length=255, 
        help_text="수업 제목", 
        verbose_name="제목"
    )
    exercise_type = models.CharField(
        max_length=255, 
        help_text="운동 종류", 
        verbose_name="운동 종류"
    )
    center = models.ForeignKey(
        Center, 
        on_delete=models.CASCADE, 
        related_name='classes', 
        verbose_name="센터"
    )
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.CASCADE, 
        related_name='classes', 
        verbose_name="강사"
    )
    schedule = models.DateTimeField(
        help_text="수업 시간", 
        verbose_name="시간"
    )
    max_attendees = models.IntegerField(
        help_text="최대 수강생 수", 
        verbose_name="최대 인원"
    )
    min_attendees = models.IntegerField(
        help_text="최소 수강생 수", 
        verbose_name="최소 인원"
    )

    def __str__(self):
        return f"{self.title} ({self.exercise_type})"

# 예약 모델
class Reservation(models.Model):
    attendee = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='reservations', 
        verbose_name="수강생"
    )
    class_reserved = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='reservations', 
        verbose_name="수업"
    )
    status = models.CharField(
        max_length=50, 
        default='reserved', 
        help_text="예약 상태", 
        verbose_name="상태"
    )
    reserved_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="예약 시간", 
        verbose_name="예약 시간"
    )
    canceled_at = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="취소 시간", 
        verbose_name="취소 시간"
    )

    def __str__(self):
        return f"{self.attendee.user.username} - {self.class_reserved.title} ({self.status})"

# 회원권 모델
class Membership(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='memberships', 
        verbose_name="수강생"
    )
    center = models.ForeignKey(
        Center, 
        on_delete=models.CASCADE, 
        related_name='memberships', 
        verbose_name="센터"
    )
    type = models.CharField(
        max_length=50, 
        help_text="회원권 종류", 
        verbose_name="종류"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="가격", 
        verbose_name="가격"
    )
    duration = models.IntegerField(
        help_text="기간 (일)", 
        verbose_name="기간"
    )

    def __str__(self):
        return f"{self.student.user.username} - {self.center.name} ({self.type})"

# 리뷰 모델
class Review(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='reviews', 
        verbose_name="수강생"
    )
    class_reviewed = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='reviews', 
        verbose_name="수업"
    )
    rating = models.IntegerField(
        help_text="평점 (1-5)", 
        verbose_name="평점"
    )
    comment = models.TextField(
        help_text="리뷰 내용", 
        verbose_name="리뷰 내용"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        help_text="작성 시간", 
        verbose_name="작성 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        help_text="수정 시간", 
        verbose_name="수정 시간"
    )

    def __str__(self):
        return f"{self.student.user.username} - {self.class_reviewed.title} ({self.rating})"
