from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import re

from .models import UserProfile

def signup(request):
    form_errors = {}
    missing_fields = []

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        nickname = request.POST.get('nickname', '')
        gender = request.POST.get('gender', '')
        birth_year = request.POST.get('birth_year', '')
        birth_month = request.POST.get('birth_month', '')
        birth_day = request.POST.get('birth_day', '')

        # 누락된 입력 체크
        if not email or not password or not repeat_password or not nickname or not gender or not birth_year or not birth_month or not birth_day:
            missing_fields.append('빠진 정보가 있는지 확인해주세요.')

        # 이메일 형식 검사
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            form_errors['email'] = '이메일 주소를 다시 확인해주세요.'
        elif User.objects.filter(email=email).exists():
            form_errors['email'] = '이미 사용 중인 이메일입니다.'

        # 비밀번호 일치 및 규칙 검사
        if password != repeat_password:
            form_errors['password'] = '비밀번호가 일치하지 않습니다.'
        elif len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[\W_]', password):
            form_errors['password'] = '비밀번호는 문자/숫자/기호를 사용하여 8자리 이상이어야 합니다.'

        # 닉네임 길이 및 중복 검사
        if len(nickname) > 8:
            form_errors['nickname'] = '닉네임은 8자 이내여야 합니다.'
        elif User.objects.filter(first_name=nickname).exists():
            form_errors['nickname'] = '중복된 닉네임입니다.'

        # 모든 조건이 충족되면 회원 가입 진행
        if not form_errors and not missing_fields:  # 이 부분의 들여쓰기 수정
            new_user = User.objects.create_user(username=email, email=email, password=password, first_name=nickname)

            # UserProfile 생성
            UserProfile.objects.create(
                user=new_user,
                # 기본값을 사용하거나 다른 기본값 설정
                alert=False,
                using_credit=0,
                remaining_credit=0,
                credit_period='',
                phone_number=''
            )

            auth_login(request, new_user)  # 자동 로그인
            messages.success(request, '회원가입 성공')
            return redirect('signInUp:login')  # 이 줄이 올바르게 들여쓰기 되어야 합니다

    return render(request, 'signup.html', {'form_errors': form_errors, 'missing_fields': missing_fields})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email', '')  # 'email' 필드에서 username 값을 가져옵니다.
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)  # 'username'으로 변경
        if user is not None:
            auth_login(request, user)
            print('로그인 성공')
            return redirect('mainPage')  # 로그인 성공 후 mainPage로 이동
        else:
            error_message = "아이디 또는 비밀번호가 잘못되었습니다."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    print('로그아웃 성공')
    return redirect('mainPage')
