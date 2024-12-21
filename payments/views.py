# payments/views.py
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
import requests
import uuid
from .models import Payment
from fiton.models import Membership, Member
from django.conf import settings

def payment_widget(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)
    member = get_object_or_404(Member, user=request.user)
    
    # 주문 ID 생성
    order_id = str(uuid.uuid4())
    
    # 결제 정보 생성
    payment = Payment.objects.create(
        order_id=order_id,
        member=member,
        membership=membership,
        amount=membership.price,
        status='READY'
    )
    
    context = {
        'clientKey': 'settings.TOSS_CLIENT_KEY',
        'customerKey': '고객_식별_키',  # 회원별 고유 키 또는 TossPayments.ANONYMOUS
        'amount': 50000,  # 결제 금액
        'order_id': 'ORDER_' + str(uuid.uuid4())[:8],  # 주문번호 생성
        'membershipName': '멤버십 이름',
        'customerName': '고객명',
        'customerEmail': '고객이메일'
    }
    
    return render(request, 'payments/payment_widget.html', context)

def payment_success(request):
    payment_key = request.GET.get('paymentKey')
    order_id = request.GET.get('orderId')
    amount = request.GET.get('amount')
    
    payment = get_object_or_404(Payment, order_id=order_id)
    
    # 결제 승인 요청
    url = "https://api.tosspayments.com/v2/payments/confirm"
    headers = {
        'Authorization': f'Basic {settings.TOSS_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'paymentKey': payment_key,
        'orderId': order_id,
        'amount': amount
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        payment.status = 'DONE'
        payment.payment_key = payment_key
        payment.save()
        return render(request, 'payments/success.html')
    else:
        return render(request, 'payments/fail.html')

def payment_fail(request):
    return render(request, 'payments/fail.html')
