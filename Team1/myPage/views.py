from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

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
        context = {
            'logged_in': True,
            'nickname': nickname,
            'remaining_credit': user_profile.remaining_credit,
            'using_credit': user_profile.using_credit,
            'credit_period': user_profile.credit_period,
            'alert': user_profile.alert,
        }
        return render(request, 'myPage.html', context)

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

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, '로그아웃 되었습니다.')
        return redirect('login')  # 로그아웃 후 로그인 페이지로 redirect
    return redirect('myPage') # GET 요청 시 마이페이지로 redirect
