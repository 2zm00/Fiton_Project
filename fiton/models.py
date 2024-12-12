from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    login_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, help_text='비밀번호 암호화')
    name = models.CharField(max_length=100, help_text='수강생, 강사는 이름, 센터는 센터명')
    USERTYPE_CHOICES = [
        ('student', '수강생'),
        ('instructor', '강사'),
        ('center', '센터'),
    ]
    usertype = models.CharField(max_length=20, choices=USERTYPE_CHOICES)
    callnum = models.CharField(max_length=100, help_text='01033334444')
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attendee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    goal_weight = models.IntegerField(null=True, blank=True)
    body_fat = models.IntegerField(null=True, blank=True)
    skeletal_muscle = models.IntegerField(null=True, blank=True)
    health_info = models.CharField(max_length=100, null=True, blank=True)
    fit_time = models.CharField(max_length=100, null=True, blank=True)
    membership_id = models.CharField(max_length=255)

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    center = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    class_field = models.CharField(max_length=255, null=True, blank=True)  # `class`는 예약어라 수정
    certification = models.CharField(max_length=255, null=True, blank=True)
    career = models.CharField(max_length=255, null=True, blank=True)
    exercise = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=255, null=True, blank=True)
    time_available = models.CharField(max_length=255, null=True, blank=True)
    account = models.CharField(max_length=255, null=True, blank=True)

class Center(models.Model):
    center_location = models.CharField(max_length=255, null=True, blank=True)
    field3 = models.CharField(max_length=255, null=True, blank=True)
    field4 = models.CharField(max_length=255, null=True, blank=True)
    field5 = models.CharField(max_length=255, null=True, blank=True)
    field6 = models.CharField(max_length=255, null=True, blank=True)

class Class(models.Model):
    exercise = models.CharField(max_length=255)
    content = models.CharField(max_length=255, null=True, blank=True)
    center = models.CharField(max_length=255, null=True, blank=True)
    progress_datetime = models.CharField(max_length=255, null=True, blank=True)
    max_attendee = models.CharField(max_length=255, null=True, blank=True)
    min_attendee = models.CharField(max_length=255, null=True, blank=True)
    reservation_available = models.CharField(max_length=255, null=True, blank=True)
    cancel_available = models.CharField(max_length=255, null=True, blank=True)
    reservation_wait = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    difficulty = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    attendee = models.ManyToManyField(Attendee)

class Reservation(models.Model):
    status = models.CharField(max_length=255, null=True, help_text='예약완료/취소/노쇼')
    datetime = models.CharField(max_length=255, null=True, blank=True)
    cancel_datetime = models.CharField(max_length=255, null=True, blank=True)
    wait_num = models.CharField(max_length=255, null=True, blank=True)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)  # `class`는 예약어라 수정

class Membership(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    exercise = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    discount = models.CharField(max_length=255, null=True, blank=True)
    time_limit = models.CharField(max_length=255, null=True, blank=True)
    TYPE_CHOICES = [
        ('1', '회원권'),
        ('0', '수업권'),
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)

class Review(models.Model):
    grade = models.CharField(max_length=255, null=True, blank=True)
    review_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    center_name = models.CharField(max_length=255, null=True, blank=True)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)  # `class`는 예약어라 수정

class Payment(models.Model):
    payment_id = models.CharField(max_length=255, primary_key=True)
    payment_amount = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True)
    refund_info = models.CharField(max_length=255, null=True, blank=True)
    center_name = models.CharField(max_length=255, null=True, blank=True)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)  # `class`는 예약어라 수정

class CenterOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=255, null=True, blank=True)

class Exercise(models.Model):
    exercise = models.CharField(max_length=255, primary_key=True)
    fitness = models.CharField(max_length=255, null=True, blank=True)
    yoga = models.CharField(max_length=255, null=True, blank=True)
    pilates = models.CharField(max_length=255, null=True, blank=True)
    rehabilitation = models.CharField(max_length=255, null=True, blank=True)
