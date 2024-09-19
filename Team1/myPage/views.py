import datetime
import json

from datetime import date, timedelta
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile
from mainPage.models import Reservation, Review

import datetime
from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def myPage(request):
    if not request.user.is_authenticated:
        # 로그인을 하지 않은 경우
        context = {
            'logged_in': False,
        }
        return render(request, 'myPage.html', context)
    else:
        # 로그인한 경우
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        nickname = request.user.first_name

        # 잔여 기간 계산
        if user_profile.credit_period:
            try:
                # credit_period가 문자열로 저장된 경우 datetime 객체로 변환
                credit_period_date = datetime.datetime.strptime(user_profile.credit_period, '%Y-%m-%d').date()
            except (TypeError, ValueError):
                # credit_period가 올바른 형식의 문자열이 아닌 경우 기본값 설정
                credit_period_date = date.today()

            today = date.today()
            remaining_days = (credit_period_date - today).days
            credit_period_display = f"{credit_period_date.strftime('%Y.%m.%d')} (D-{remaining_days})"
        else:
            credit_period_display = "멤버십을 구매하세요"

        # 예약 내역 조회
        reservations = Reservation.objects.filter(user_id=request.user)

        context = {
            'logged_in': True,
            'nickname': nickname,
            'remaining_credit': user_profile.remaining_credit or "멤버십을 구매하세요",
            'using_credit': user_profile.using_credit or 0,
            'credit_period': credit_period_display,
            'alert': user_profile.alert,
            'reservations': reservations,
        }
        return render(request, 'myPage.html', context)

@login_required
def my_reservation(request):
    # 로그인한 사용자의 예약 정보를 가져옴
    user_reservations = Reservation.objects.filter(user_id=request.user.id)
    
    # 예약이 없을 경우를 대비하여 예약 내역 확인
    if not user_reservations.exists():
        message = "현재 예약된 클래스가 없습니다."
    else:
        message = None

    # 템플릿에 예약 내역과 메시지를 전달
    return render(request, 'my_reservation.html', {
        'reservations': user_reservations,
        'message': message
    })

@login_required
def cancel_reservation(request, reservation_id):
    # 예약 객체 가져오기
    reservation = get_object_or_404(Reservation, id=reservation_id, user_id=request.user)

    # 크레딧 반환 처리
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.remaining_credit != '프리미엄 멤버십':
        try:
            remaining_credit = int(user_profile.remaining_credit)
            user_profile.remaining_credit = remaining_credit + reservation.class_id.credit_num
        except ValueError:
            # 만약 크레딧이 숫자가 아닐 경우, 기본 크레딧을 반환
            user_profile.remaining_credit = reservation.class_id.credit_num

        # 소진 크레딧도 복구
        if user_profile.using_credit:
            try:
                using_credit = int(user_profile.using_credit)
                user_profile.using_credit = max(0, using_credit - reservation.class_id.credit_num)
            except ValueError:
                # 소진 크레딧이 숫자가 아닐 경우 기본값 0으로 설정
                user_profile.using_credit = 0

        user_profile.save()

    # 예약 내역 삭제
    reservation.delete()

    # 취소 완료 메시지
    messages.success(request, '예약이 취소되었습니다.')

    return HttpResponseRedirect(reverse('my_reservation'))

@login_required
def write_review(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user_id=request.user)
    class_instance = reservation.class_id

    if request.method == 'POST':
        # 리뷰 저장
        star = request.POST.get('star')
        detail = request.POST.get('detail')
        keywords = request.POST.getlist('keyword')

        Review.objects.create(
            user_id=request.user,
            class_id=class_instance,
            reservation_id=reservation,
            star=star,
            keyword=','.join(keywords),
            detail=detail
        )

        messages.success(request, '리뷰가 작성되었습니다.')

        # 리뷰가 등록된 후 center_detail로 리다이렉트
        return redirect('center_detail', center_id=class_instance.center_data_id)

    return render(request, 'write_review.html', {'reservation': reservation})


@login_required
def update_alert(request):
    if request.method == 'POST':
        alert_status = request.POST.get('alert', 'off')  # 'on' 또는 'off'
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.alert = (alert_status == 'on')
        user_profile.save()
        messages.success(request, '푸시 알림 설정이 저장되었습니다.')
        return redirect('myPage')  # 마이페이지로 redirect
    return redirect('myPage')


def membership(request):
    logged_in = request.user.is_authenticated
    return render(request, 'membership.html', {'logged_in': logged_in})


@login_required
def membership_purchase(request, product):
    return render(request, 'membership_purchase.html', {'product': product})


@login_required
def purchase_membership(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = data.get('product')

        # DB에서 UserProfile을 가져옴
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # 현재 날짜 가져옴
        today = date.today()

        # 제품에 따라 UserProfile 업데이트
        if product == '프리미엄 멤버십':
            # 프리미엄 멤버십 구매 시 모든 크레딧 초기화
            user_profile.remaining_credit = '프리미엄 멤버십'
            user_profile.using_credit = '없음'  # 프리미엄 멤버십은 소진 크레딧을 '없음'으로 설정
        elif product in ['5 크레딧', '3 크레딧', '1 크레딧']:
            # 프리미엄 멤버십을 가지고 있는 경우 크레딧 추가 X
            if user_profile.remaining_credit == '프리미엄 멤버십':
                # 프리미엄 멤버십 상태에서는 크레딧을 추가 X
                return JsonResponse({'success': False})

            # 숫자만 추출하여 크레딧 수를 더함
            additional_credits = int(product.split()[0])

            # 현재 남아있는 크레딧이 숫자인지 확인하고 합산
            if isinstance(user_profile.remaining_credit, int):
                user_profile.remaining_credit += additional_credits
            elif isinstance(user_profile.remaining_credit, str) and user_profile.remaining_credit.isdigit():
                user_profile.remaining_credit = int(user_profile.remaining_credit) + additional_credits
            else:
                user_profile.remaining_credit = additional_credits

            user_profile.using_credit = 0  # 구매 후 소진 크레딧은 0으로 설정

        # 결제일로부터 6개월 후로 잔여 기간 설정
        user_profile.credit_period = today + timedelta(days=180)

        user_profile.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, '로그아웃 되었습니다.')
        return redirect('login')  # 로그아웃 후 로그인 페이지로 redirect
    return redirect('myPage')  # GET 요청 시 마이페이지로 redirect
