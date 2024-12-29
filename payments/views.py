# payments/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
import requests
import uuid
import base64
from .models import Payment
from fiton.models import Membership, Member, Center, MembershipOwner, ClassTicketOwner, ClassTicket, Class
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

############## 페이지 렌더링


# 멤버쉽 결제 
def membership_payment_detail(request, center_pk, membership_pk):
    center = get_object_or_404(Center, pk=center_pk)
    member = get_object_or_404(Member, user=request.user)
    membership = get_object_or_404(Membership, id=membership_pk)

    success_url = request.build_absolute_uri(
        reverse('payments:membership_payment_success', kwargs={'center_pk': center_pk})
    )
    fail_url = request.build_absolute_uri(
        reverse('payments:membership_payment_fail', kwargs={'center_pk': center_pk})
    )

    order_id = f"ORDER_{uuid.uuid4().hex}"
    payment = Payment.objects.create(
        order_id=order_id,
        amount=membership.price,
        status='READY',
        member=member,
        item_type='membership',
        item_id=membership_pk
    )

    context = {
        'center': center,
        'item': membership,
        'item_name': membership.name,
        'client_key': settings.TOSS_CLIENT_KEY,
        'order_id': payment.order_id,
        'amount': membership.price,
        'customer_name': request.user.username,
        'success_url': success_url,
        'fail_url': fail_url,
    }

    return render(request, 'payments/payment/checkout.html', context)

# 수강권 결제
def classticket_payment_detail(request, class_pk, classticket_pk):
    classes = get_object_or_404(Class, pk=class_pk)
    member = get_object_or_404(Member, user=request.user)
    class_ticket = get_object_or_404(ClassTicket, id=classticket_pk)

    success_url = request.build_absolute_uri(
        reverse('payments:classticket_payment_success', kwargs={'class_pk': class_pk})
    )
    fail_url = request.build_absolute_uri(
        reverse('payments:classticket_payment_fail', kwargs={'class_pk': class_pk})
    )

    order_id = f"ORDER_{uuid.uuid4().hex}"
    payment = Payment.objects.create(
        order_id=order_id,
        amount=class_ticket.price,
        status='READY',
        member=member,
        item_type='classticket',
        item_id=classticket_pk
    )

    context = {
        'item': class_ticket,
        'item_name': class_ticket.class_type.name,
        'client_key': settings.TOSS_CLIENT_KEY,
        'order_id': payment.order_id,
        'amount': class_ticket.price,
        'customer_name': request.user.username,
        'success_url': success_url,
        'fail_url': fail_url,
    }

    return render(request, 'payments/payment/checkout.html', context)

def membership_payment_success(request, center_pk):
    payment_key = request.GET.get('paymentKey')
    order_id = request.GET.get('orderId')
    amount = request.GET.get('amount')
    
    center = get_object_or_404(Center, pk=center_pk)
    payment = get_object_or_404(Payment, order_id=order_id)
    
    
    try:
        # 결제 금액 검증
        if payment.amount != int(amount):
            return render(request, 'payments/fail.html', {
                'error_code': 'AMOUNT_MISMATCH',
                'error_message': '결제 금액이 일치하지 않습니다.'
            })
        
        # 시크릿 키 인코딩
        secret_key = settings.TOSS_SECRET_KEY
        secret_key_with_colon = f"{secret_key}:"
        encoded_secret_key = base64.b64encode(secret_key_with_colon.encode()).decode()
            
        # 결제 승인 요청
        url = "https://api.tosspayments.com/v1/payments/confirm"
        headers = {
            'Authorization': f'Basic {encoded_secret_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'paymentKey': payment_key,
            'orderId': order_id,
            'amount': amount
        }
        
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            # 결제 성공 처리
            payment.status = 'DONE'
            payment.payment_key = payment_key
            payment.save()
            
            # 회원권 소유권 생성
            membership = get_object_or_404(Membership, id=payment.item_id)
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=membership.duration)
            
            MembershipOwner.objects.create(
                member=payment.member,
                center=membership.center,
                start_date=start_date,
                end_date=end_date
            )
            
            context = {
                'center': center,
                'response': response_data,
                'payment': payment
            }
            return render(request, 'payments/payment/success.html', context)
        else:
            # API 요청 실패 처리
            error_msg = response_data.get('message', '결제 승인 중 오류가 발생했습니다.')
            return render(request, 'payments/fail.html', {
                'error_code': response_data.get('code'),
                'error_message': error_msg
            })
            
    except Payment.DoesNotExist:
        return render(request, 'payments/fail.html', {
            'error_code': 'INVALID_ORDER',
            'error_message': '유효하지 않은 주문입니다.'
        })
    except Exception as e:
        return render(request, 'payments/fail.html', {
            'error_code': 'SYSTEM_ERROR',
            'error_message': str(e)
        })

def classticket_payment_success(request, class_pk): 
    payment_key = request.GET.get('paymentKey')
    order_id = request.GET.get('orderId')
    amount = request.GET.get('amount')
    
    payment = get_object_or_404(Payment, order_id=order_id)
    
    try:
        # 결제 금액 검증
        if payment.amount != int(amount):
            return render(request, 'payments/fail.html', {
                'error_code': 'AMOUNT_MISMATCH',
                'error_message': '결제 금액이 일치하지 않습니다.'
            })
        
        # 시크릿 키 인코딩
        secret_key = settings.TOSS_SECRET_KEY
        secret_key_with_colon = f"{secret_key}:"
        encoded_secret_key = base64.b64encode(secret_key_with_colon.encode()).decode()
            
        # 결제 승인 요청
        url = "https://api.tosspayments.com/v1/payments/confirm"
        headers = {
            'Authorization': f'Basic {encoded_secret_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'paymentKey': payment_key,
            'orderId': order_id,
            'amount': amount
        }
        
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            payment.status = 'DONE'
            payment.payment_key = payment_key
            payment.save()
            
            # 수업권 소유권 생성/업데이트
            class_ticket = get_object_or_404(ClassTicket, id=payment.item_id)
            ticket_owner, created = ClassTicketOwner.objects.get_or_create(
                member=payment.member,
                class_ticket=class_ticket,
                defaults={'quantity': class_ticket.ticket_quantity}
            )
            
            if not created:
                ticket_owner.quantity += class_ticket.ticket_quantity
                ticket_owner.save()
            
            context = {
                'response': response_data,
                'payment': payment
            }
            return render(request, 'payments/payment/success.html', context)
        else:
            # API 요청 실패 처리
            error_msg = response_data.get('message', '결제 승인 중 오류가 발생했습니다.')
            return render(request, 'payments/fail.html', {
                'error_code': response_data.get('code'),
                'error_message': error_msg
            })
            
    except Payment.DoesNotExist:
        return render(request, 'payments/fail.html', {
            'error_code': 'INVALID_ORDER',
            'error_message': '유효하지 않은 주문입니다.'
        })
    except Exception as e:
        return render(request, 'payments/fail.html', {
            'error_code': 'SYSTEM_ERROR',
            'error_message': str(e)
        })

def membership_payment_fail(request, center_pk):
    error_code = request.GET.get('code')
    error_msg = request.GET.get('message')
    return render(request, 'payments/fail.html', {
        'error_code': error_code,
        'error_message': error_msg,
        'center': get_object_or_404(Center, pk=center_pk)
    })

def classticket_payment_fail(request, class_pk):
    error_code = request.GET.get('code')
    error_msg = request.GET.get('message')
    return render(request, 'payments/fail.html', {
        'error_code': error_code,
        'error_message': error_msg,
        'classes': get_object_or_404(Class, pk=class_pk)
    })
