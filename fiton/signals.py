from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    User, Member, CenterOwner, Exercise, Center, Instructor, InstructorApplication,Notification,
    Class, ClassTicket, ClassTicketOwner,Class_type, Reservation, Review, Membership, MembershipOwner
)


@receiver(post_save, sender=Reservation)
def notify_reservation_status_change(sender, instance, created, **kwargs):
    # 예약 상태가 'reserved'로 변경된 경우
    if instance.status == 'reserved' and not created:
        Notification.objects.create(
            user=instance.member.user,
            message=f"{instance.member.user.name}님, 대기 중이었던 {instance.class_reserved.name} 수업의 예약이 확정되었습니다!"
        )
    elif instance.status == 'reservation canceled' and not created:
        Notification.objects.create(
            user=instance.member.user,
            message=f"{instance.member.user.name}님의 {instance.class_reserved.name} 수업의 예약이 취소되었습니다!"
        )
    elif instance.status == 'class canceled' and not created:
        Notification.objects.create(
            user=instance.member.user,
            message=f"{instance.member.user.name}님의 {instance.class_reserved.name} 수업이 취소되었습니다, 수업티켓은 다시 제공 되었습니다!"
        )
    elif instance.status == 'class start' and not created:
        Notification.objects.create(
            user=instance.member.user,
            message=f"{instance.member.user.name}님의 {instance.class_reserved.name} 수업이 시작되셨습디다!"
        )
   
@receiver(post_save, sender=Reservation)
def notify_reservation_status_create(sender, instance, created, **kwargs):
    
    if created:
        Notification.objects.create(
            user=instance.member.user,
            message=f"{instance.member.user.name}님이 신청하신 {instance.class_reserved.name} 수업의 예약이 확정되었습니다!"

        )
        if instance.status =='reserved':
            Notification.objects.create(
                user=instance.class_reserved.instructor.user,
                message=f"{instance.member.user.name}님이 {instance.class_reserved.name} 수업을 예약 하셨습니다!"
                
            )
        else:
            Notification.objects.create(
                user=instance.class_reserved.instructor.user,
                message=f"{instance.member.user.name}님이 {instance.class_reserved.name} 수업을 예약 대기 하셨습니다!"
                
            )


@receiver(post_save, sender=InstructorApplication)
def notify_application_status_change(sender, instance, created, **kwargs):
    
    if instance.status == 'approved' and not created:
        Notification.objects.create(
            user=instance.instructor.user,
            message=f"{instance.instructor.user.name}님, 등록 요청한 {instance.center.name} 센터에 등록 되셨습니다!"
        )
    elif instance.status == 'rejected' and not created:
        Notification.objects.create(
            user=instance.instructor.user,
            message=f"{instance.instructor.user.name}님, 등록 요청한 {instance.center.name} 센터에 거부 되셨습니다!"
        )
    
@receiver(post_save, sender=InstructorApplication)
def notify_application_status_create(sender, instance, created, **kwargs):
   
    if created:
        Notification.objects.create(
            user=instance.center.owner.user,
            message=f"{instance.instructor.user.name}님이 {instance.center.name} 센터에 강사 등록 요청을 했습니다!"

        )

@receiver(post_save, sender=Class)
def notify_class_deleted(sender, instance,created, **kwargs):
    if instance.is_deleted and not created:
        Notification.objects.create(
            user=instance.instructor.user,
            message=f"{instance.instructor.user.name}님의 {instance.name}수업이 삭제 되셨습니다!"
        )
        
    