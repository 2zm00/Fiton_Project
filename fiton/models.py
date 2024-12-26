from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import timedelta,date,datetime

# 기본 유저 모델 확장
class User(AbstractUser):
    ROLE_CHOICES = (
        ('member', '수강생'),
        ('instructor', '강사'),
        ('centerowner', '센터장'),
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='member', 
        verbose_name="역할"
    )
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        verbose_name="전화번호"
    )
    image = models.ImageField(
        upload_to='profile_images/', 
        null=True, 
        blank=True, 
        verbose_name="프로필 이미지"
    )
    name = models.CharField(
        max_length=10,
        verbose_name="이름"
    )
    gender = models.CharField(
        max_length=50, 
        choices=(('male','남자'),('female','여자'),('other','선택 안 함')),
        verbose_name="성별"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="생년월일",
    )
    first_name = None  # 성 필드 제거
    last_name = None   # 이름 필드 제거
    # email = None #이메일 필드 제거
class Notification(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name="사용자"
    )
    message = models.TextField(verbose_name="알림 메시지")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")

    def __str__(self):
        return f"알림: {self.message[:30]}... ({'읽음' if self.is_read else '읽지 않음'})"

# 수강생 모델
class Member(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="사용자"
    )
    height = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="키"
    )
    weight = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="체중"
    )
    goal_weight = models.IntegerField(
        null=True, 
        blank=True,  
        verbose_name="목표 체중"
    )
    body_fat = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="체지방률"
    )
    skeletal_muscle = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="골격근량"
    )
    health_info = models.TextField(
        null=True, 
        blank=True,  
        verbose_name="건강 정보"
    )

    def __str__(self):
        return f"{self.user.name} (수강생)"

# 센터장 모델
class CenterOwner(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="사용자"
    )
    business_registration_number=models.IntegerField(
        verbose_name="사업자 등록번호"
    )

    def __str__(self):
        return f"{self.user.name} (센터장)"

# 운동 종목 모델
class Exercise(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="운동 종목"
    )

    def __str__(self):
        return self.name



# 센터 모델
class Center(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="센터 이름"
    )
    #지도기능
    location = models.CharField(
        max_length=255, 
        verbose_name="센터 위치"
    )
    owner = models.ForeignKey(
        CenterOwner, 
        on_delete=models.CASCADE, 
        related_name='centers',
        verbose_name="센터장"
    )
    
    exercise = models.ManyToManyField(
        Exercise,
        verbose_name="운동 종목"
    )

    def __str__(self):
        return f"{self.name} ({self.location})"


# 강사 모델
class Instructor(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="사용자"
    )
    center = models.ManyToManyField(
        Center,
        related_name='instructors',
        verbose_name="등록된 센터"
    )
    expertise = models.CharField(
        max_length=255,  
        verbose_name="전문 분야"
    )
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0, 
        verbose_name="평균 별점"
    )
    available_hours = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="수업 가능 시간"
    )
    introduction = models.TextField(
        null=True, 
        blank=True,  
        verbose_name="강사 자기소개서"
    )
    certification = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="자격증"
    )
    career = models.TextField(
        null=True, 
        blank=True,  
        verbose_name="경력"
    )

    def __str__(self):
        return f"{self.user.name} (강사)"

#이름변경 강사 등록 모델
class InstructorApplication(models.Model):
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.CASCADE, 
        related_name="applications", 
        verbose_name="강사"
    )
    center = models.ForeignKey(
        Center, 
        on_delete=models.CASCADE, 
        related_name="applications", 
        verbose_name="센터"
    )
    status = models.CharField(
        max_length=20, 
        choices=(('pending', '대기 중'), ('approved', '승인됨'), ('rejected', '거부됨')), 
        default='pending', 
        verbose_name="상태"
    )
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="신청일")

    def __str__(self):
        return f"{self.instructor.user.name} -> {self.center.name} ({self.status})"
    
class Class_type(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="수업 종류"
    )

    def __str__(self):
        return self.name
# 수업 모델
class Class(models.Model):
    name = models.CharField(
        max_length=255, 
        verbose_name="제목"
    )
    center = models.ForeignKey(
        Center, 
        on_delete=models.CASCADE, 
        related_name='classes',
        verbose_name="진행 센터"
    )
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.CASCADE, 
        related_name='classes',
        verbose_name="강사"
    )
    #수업종류는 center.exercise.name

    # 수업종류는 1:1/ 1:다 및 수업권 구분할 수 있는 정보가 필요함.
    class_type=models.ForeignKey(
        Class_type,
        on_delete=models.CASCADE, 
        related_name='classes',
        verbose_name="수업 종류"
    )

    content = models.TextField(
        null=True, 
        blank=True,  
        verbose_name="수업 내용"
    )

    location = models.TextField(
        max_length=255,
        verbose_name="수업 장소"
    )
    #알림 로직 시 필요할 것 (예정)
    start_class = models.DateTimeField(
        verbose_name="수업 진행 일시"
    )
    reservation_permission = models.DateTimeField(
        verbose_name="예약 가능 시간",
        null=True,  
        blank=True
    )
    cancellation_permission = models.DateTimeField(
        verbose_name="예약 취소 날짜",
        null=True, 
        blank=True
    )

    max_member = models.IntegerField(
        verbose_name="최대 인원"
    )
    min_memeber = models.IntegerField(
        verbose_name="최소 인원"
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name="삭제 여부"
    )
    

    def __str__(self):
        return f"{self.name} ({self.center.exercise.name})"
    
    
    def is_reservation_allowed(self):
        """현재 시간이 예약 가능 시간 이후인지 확인"""
        if not self.reservation_permission:
            return False
        return datetime.now() >= self.reservation_permission

    def delete(self, *args, **kwargs):
        # 실제 삭제 대신 is_deleted를 True로 설정
        self.is_deleted = True
        self.save()
 
class ClassTicket(models.Model):
    class_type = models.ForeignKey(
        Class_type, 
        on_delete=models.CASCADE, 
        related_name='class_ticket',
        verbose_name="수업 종류"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="가격"
    )
    ticket_quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="수업권 횟수"
    ) 

class ClassTicketOwner(models.Model):
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        related_name='class_ticket_owner',
        verbose_name="수강생"
    )
    class_ticket = models.ForeignKey(
        ClassTicket, 
        on_delete=models.CASCADE, 
        related_name='class_ticket_owner',
        verbose_name="수업권"
    )
    quantity=models.PositiveIntegerField(
        default=0,
        verbose_name="수업권 개수"
    )
    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name="사용한 수업권 횟수"
    ) 
# 예약 모델
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('reserved', '예약됨'),
        ('Waiting for the reservation', '예약대기중'),
        ('reservation canceled', '예약취소'),
        ('Reservation Completed', '예약 종료'),
        ('Class Completed', '수업 종료'),
        ('class canceled','수업 취소'),
        ('class start','수업 시작')
    )

    member = models.ForeignKey(
        Member, 
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
        choices=STATUS_CHOICES,
        default='reserved', 
        verbose_name="상태"
    )
    reserved_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="예약 시간"
    )
    canceled_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="취소 시간"
    )

    def __str__(self):
        return f"{self.member.user.name} - {self.class_reserved.name} ({self.status})"



# 리뷰 모델
class Review(models.Model):
    member = models.ForeignKey(
        Member, 
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
        verbose_name="평점"
    )
    comment = models.TextField(
        verbose_name="리뷰 내용"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  
        verbose_name="작성 시간"
    )
    updated_at = models.DateTimeField(
        auto_now=True,  
        verbose_name="수정 시간"
    )

    def __str__(self):
        return f"{self.student.user.name} - {self.class_reviewed.name} ({self.rating})"

# 회원권 모델
class Membership(models.Model):
    center = models.ForeignKey(
        Center,
        on_delete=models.CASCADE,
        related_name='center_memberships',
        verbose_name="센터"
    ) 
    name = models.CharField(
        max_length=255,
        verbose_name="회원권 이름"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="가격"
    )
    duration = models.IntegerField(
        verbose_name="기간(일)"
    )


    def __str__(self):
        return f"{self.name} - {self.center.name}"

# 수강생 회원권 소유 모델
class MembershipOwner(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='owned_memberships',
        verbose_name="수강생"
    )
    center = models.ForeignKey(
        Center,
        on_delete=models.CASCADE,
        related_name='owned_memberships',
        verbose_name="센터"
    ) 
    start_date = models.DateField(
        auto_now_add=True,
        verbose_name="시작 날짜"
    )
    end_date = models.DateField(
        verbose_name="종료 날짜"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="활성화 여부"
    )

    def save(self, *args, **kwargs):
        # 종료 날짜를 시작 날짜 + duration으로 설정
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.membership.duration)

        # 종료 날짜를 기반으로 활성화 여부 업데이트
        # w종료날짜가 되면 삭제되게 구현하기
        # self.is_active = date.today() <= self.end_date

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.user.name} - {self.membership.name}"

