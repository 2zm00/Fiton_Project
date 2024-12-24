# payments/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
import requests
import uuid
import base64
from .models import Payment
from fiton.models import Membership, Member, Center, MembershipOwner, ClassTicketOwner, ClassTicket
from django.conf import settings

############## 페이지 렌더링



def payment_detail(request, source, center_pk, item_type, item_pk):
	#url에 전송할 데이터 함수 정의
    center = get_object_or_404(Center, pk=center_pk)
    member = get_object_or_404(Member, user=request.user)

    # 결제 종류에 따른 아이템 분류
    if item_type == 'membership':
        item = get_object_or_404(Membership, id=item_pk)
        item_name = item.name
        owner_model = MembershipOwner
    elif item_type == 'classticket':
        item = get_object_or_404(ClassTicket, id=item_pk)
        item_name = item.class_type.name
        owner_model = ClassTicketOwner


    success_url = request.build_absolute_uri(
        reverse('payments:payment_success', kwargs={'center_pk': center_pk})
    )
    fail_url = request.build_absolute_uri(
        reverse('payments:payment_fail', kwargs={'center_pk': center_pk})
    )

    # 결제 정보 정의
    order_id = f"ORDER_{uuid.uuid4().hex}"
    payment = Payment.objects.create(
        order_id=order_id,
        amount=item.price,
        status='READY',
        member=member,
        item_type=item_type,
        item_id=item_pk
    )
    # 템플릿에 전송할 데이터 정의
    context = {
        'center': center,
        'item': item,
        'item_name': item_name,
        'client_key': settings.TOSS_CLIENT_KEY,
        'order_id': payment.order_id,
        'amount': item.price,
        'customer_name': request.user.username,
        'success_url': success_url,
        'fail_url': fail_url,
    }

    return render(request, 'payments/payment/checkout.html', context)


def payment_success(request, center_pk):


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
        
        context = {
            'center': center,
            'response': response_data,
            'payment': payment
        }

        if response.status_code == 200:
            # 결제 성공 처리
            payment.status = 'DONE'
            payment.payment_key = payment_key
            payment.save()
            
            # 결제 유형에 따른 소유권 생성
            if payment.item_type == 'membership':
                membership = get_object_or_404(Membership, id=payment.item_id)
                MembershipOwner.objects.create(
                    member=payment.member,
                    membership=membership
                )
            else:  # classticket
                class_ticket = get_object_or_404(ClassTicket, id=payment.item_id)
                ticket_owner = ClassTicketOwner.objects.get_or_create(
                    member=payment.member,
                    class_ticket=class_ticket,
                    defaults={'quantity':  class_ticket.ticket_quantity}
                    )
                ticket_owner.quantity += class_ticket.ticket_quantity
                ticket_owner.save()
            
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


def payment_fail(request, center_pk):
    error_code = request.GET.get('code')
    error_msg = request.GET.get('message')
    return render(request, 'payments/fail.html', {
        'error_code': error_code,
        'error_message': error_msg
    })
