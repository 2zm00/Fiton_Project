# payments/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
import requests
import uuid
from .models import Payment
from fiton.models import Membership, Member, Center
from django.conf import settings

############## 페이지 렌더링



def payment_detail(request, center_pk, membership_pk):
	#url에 전송할 데이터 함수 정의
    center = get_object_or_404(Center, pk=center_pk)
    membership = get_object_or_404(Membership, id=membership_pk)
    member = get_object_or_404(Member, user=request.user)

    success_url = request.build_absolute_uri(
        reverse('payments:payment_success', kwargs={'center_pk': center_pk})
    )
    fail_url = request.build_absolute_uri(
        reverse('payments:payment_fail', kwargs={'center_pk': center_pk})
    )
    order_id = f"ORDER_{uuid.uuid4().hex}"
    payment = Payment.objects.create(
        order_id=order_id,
        amount=membership.price,
        status='READY',
        member=member,
        membership=membership
    )
    context = {
        'center': center,
        'membership': membership,
        'client_key': settings.TOSS_CLIENT_KEY,
        'order_id': payment.order_id,
        'amount': membership.price,
        'customer_name': request.user.username,
        'success_url': success_url,
        'fail_url': fail_url,
    }

    return render(request, 'payments/payment/checkout.html', context)


def payment_success(request, center_pk):
    import base64

    payment_key = request.GET.get('paymentKey')
    order_id = request.GET.get('orderId')
    amount = request.GET.get('amount')
    
    center = get_object_or_404(Center, pk=center_pk)
    payment = get_object_or_404(Payment, order_id=order_id)
    membership = payment.membership

    
    
    try:
        payment = Payment.objects.get(order_id=order_id)
        
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
            'membership': membership,
            'response': response_data,
            'payment': payment
        }

        if response.status_code == 200:
            # 결제 성공 처리
            payment.status = 'DONE'
            payment.payment_key = payment_key
            payment.save()
            
            # 멤버십 활성화 처리
            membership = payment.membership
            member = payment.member
            # 멤버십 활성화 로직 추가
            
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
