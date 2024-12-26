# Generated by Django 5.1.3 on 2024-12-26 01:15

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='수업 종류')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='운동 종목')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('member', '수강생'), ('instructor', '강사'), ('centerowner', '센터장')], default='member', max_length=20, verbose_name='역할')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='전화번호')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images/', verbose_name='프로필 이미지')),
                ('name', models.CharField(max_length=10, verbose_name='이름')),
                ('gender', models.CharField(choices=[('male', '남자'), ('female', '여자'), ('other', '선택 안 함')], max_length=50, verbose_name='성별')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='생년월일')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CenterOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_registration_number', models.IntegerField(verbose_name='사업자 등록번호')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='센터 이름')),
                ('location', models.CharField(max_length=255, verbose_name='센터 위치')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centers', to='fiton.centerowner', verbose_name='센터장')),
                ('exercise', models.ManyToManyField(to='fiton.exercise', verbose_name='운동 종목')),
            ],
        ),
        migrations.CreateModel(
            name='ClassTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='가격')),
                ('ticket_quantity', models.PositiveIntegerField(default=1, verbose_name='수업권 횟수')),
                ('class_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_ticket', to='fiton.class_type', verbose_name='수업 종류')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(max_length=255, verbose_name='전문 분야')),
                ('average_rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='평균 별점')),
                ('available_hours', models.TextField(blank=True, null=True, verbose_name='수업 가능 시간')),
                ('introduction', models.TextField(blank=True, null=True, verbose_name='강사 자기소개서')),
                ('certification', models.TextField(blank=True, null=True, verbose_name='자격증')),
                ('career', models.TextField(blank=True, null=True, verbose_name='경력')),
                ('center', models.ManyToManyField(related_name='instructors', to='fiton.center', verbose_name='등록된 센터')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='제목')),
                ('content', models.TextField(blank=True, null=True, verbose_name='수업 내용')),
                ('location', models.TextField(max_length=255, verbose_name='수업 장소')),
                ('start_class', models.DateTimeField(verbose_name='수업 진행 일시')),
                ('reservation_permission', models.DateTimeField(blank=True, null=True, verbose_name='예약 가능 시간')),
                ('cancellation_permission', models.DateTimeField(blank=True, null=True, verbose_name='예약 취소 날짜')),
                ('max_member', models.IntegerField(verbose_name='최대 인원')),
                ('min_memeber', models.IntegerField(verbose_name='최소 인원')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='fiton.center', verbose_name='진행 센터')),
                ('class_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='fiton.class_type', verbose_name='수업 종류')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='fiton.instructor', verbose_name='강사')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', '대기 중'), ('approved', '승인됨'), ('rejected', '거부됨')], default='pending', max_length=20, verbose_name='상태')),
                ('applied_at', models.DateTimeField(auto_now_add=True, verbose_name='신청일')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='fiton.center', verbose_name='센터')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='fiton.instructor', verbose_name='강사')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='키')),
                ('weight', models.IntegerField(blank=True, null=True, verbose_name='체중')),
                ('goal_weight', models.IntegerField(blank=True, null=True, verbose_name='목표 체중')),
                ('body_fat', models.IntegerField(blank=True, null=True, verbose_name='체지방률')),
                ('skeletal_muscle', models.IntegerField(blank=True, null=True, verbose_name='골격근량')),
                ('health_info', models.TextField(blank=True, null=True, verbose_name='건강 정보')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='ClassTicketOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='수업권 개수')),
                ('used_count', models.PositiveIntegerField(default=0, verbose_name='사용한 수업권 횟수')),
                ('class_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_ticket_owner', to='fiton.classticket', verbose_name='수업권')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_ticket_owner', to='fiton.member', verbose_name='수강생')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='회원권 이름')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='가격')),
                ('duration', models.IntegerField(verbose_name='기간(일)')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='center_memberships', to='fiton.center', verbose_name='센터')),
            ],
        ),
        migrations.CreateModel(
            name='MembershipOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='시작 날짜')),
                ('end_date', models.DateField(verbose_name='종료 날짜')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화 여부')),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_memberships', to='fiton.center', verbose_name='센터')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_memberships', to='fiton.member', verbose_name='수강생')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='알림 메시지')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('is_read', models.BooleanField(default=False, verbose_name='읽음 여부')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('reserved', '예약됨'), ('Waiting for the reservation', '예약대기중'), ('reservation canceled', '예약취소'), ('Reservation Completed', '예약 종료'), ('Class Completed', '수업 종료'), ('class canceled', '수업 취소'), ('class start', '수업 시작')], default='reserved', max_length=50, verbose_name='상태')),
                ('reserved_at', models.DateTimeField(auto_now_add=True, verbose_name='예약 시간')),
                ('canceled_at', models.DateTimeField(blank=True, null=True, verbose_name='취소 시간')),
                ('class_reserved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='fiton.class', verbose_name='수업')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='fiton.member', verbose_name='수강생')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(verbose_name='평점')),
                ('comment', models.TextField(verbose_name='리뷰 내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 시간')),
                ('class_reviewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='fiton.class', verbose_name='수업')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='fiton.member', verbose_name='수강생')),
            ],
        ),
    ]
