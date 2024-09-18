from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
import logging
from django.template.loader import get_template, TemplateDoesNotExist
import re
import os
from django.conf import settings
from .models import Class, Reservation, Review
from myPage.models import UserProfile
from django.contrib.auth.models import User
import csv
from django.db import transaction

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(BASE_DIR, 'yongsan.csv')


# 메인페이지 로딩
def mainPage(request):
    return render(request, 'mainPage.html')


# 지역,운동종류에 맞게 검색하기
def filter_centers(request):
    dong = request.GET.get('dong')
    exercise = request.GET.get('exercise')

    # CSV 파일 로드
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    print(df.columns)

    if 'id' not in df.columns:
        df['id'] = df.index + 1  # 고유 ID 필드 생성

    # 페이지 첫 로드 시 랜덤 5개 반환
    if not dong and not exercise:
        filtered_df = df.sample(5)
    else:
        # 필터링 로직
        if dong and exercise:
            filtered_df = df[(df['동/읍'] == dong) & (df['운동 종류'].str.contains(re.escape(exercise), case=False))]
        elif dong:
            filtered_df = df[df['동/읍'] == dong]
        elif exercise:
            filtered_df = df[df['운동 종류'].str.contains(re.escape(exercise), case=False)]

    # NaN 값을 빈 문자열로 대체
    filtered_df = filtered_df.fillna('')

    # 결과 데이터 추출 (센터 이름과 사진 링크만 포함)
    results = filtered_df[['id', '센터 이름', '사진','주소']].to_dict('records')

    return JsonResponse(results, safe=False)


# 특정 체육관 클릭시 상세페이지 넘어가게 하기
def center_detail(request, center_id):
    # CSV 파일 로드
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    # center_id로 해당 센터 데이터 검색
    try:
        center_data = df[df['id'] == center_id].iloc[0]
    except IndexError:
        raise Http404("센터를 찾을 수 없습니다.")

    context = {
        'center': {
            'id': center_data['id'],
            'name': center_data['센터 이름'],
            'address': center_data['주소'],
            'phone': center_data['전화번호'],
            'latitude': center_data['위도'],
            'longitude': center_data['경도'],
            'image_url': center_data['사진'],
            'number': center_data['전화번호'],
            'time': center_data['운영 시간'],
            'detail_info': center_data['센터 정보(설명)'],
            'free': center_data['무료로 이용할 수 있어요'],
            'supplies': center_data['따로 준비하면 좋아요']
        },
        'kakao_api_key': settings.KAKAO_API_JS_KEY,  # API 키를 템플릿으로 전달
    }

    return render(request, 'detailed_center.html', context)


# 기관별 스케줄 가져오기
def get_schedule(request, center_id):
    # Fetch all classes associated with the given center_id
    classes = Class.objects.filter(center_data_id=center_id).values(
        'id', 'time', 'detail', 'credit_num', 'duration', 'teacher'
    )

    # Convert queryset to list of dictionaries
    classes_list = list(classes)

    return JsonResponse(classes_list, safe=False)


# 센터이름찾기
def get_center_name_by_id(center_id):
    with open('yongsan.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row['id'] == str(center_id):
                return row['센터 이름']

    return None  # 해당 ID에 대한 센터 이름이 없을 경우


def reservation_view(request):
    class_id = request.GET.get('classId')
    class_instance = get_object_or_404(Class, id=class_id)
    center_name = get_center_name_by_id(class_instance.center_data_id)

    # CSV 파일에서 센터 이미지를 가져옴
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    center_image_url = df[df['id'] == class_instance.center_data_id]['사진'].values[0]  # 이미지 URL 추출

    if request.method == 'POST':
        with transaction.atomic():
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']

            user, created = User.objects.get_or_create(email=email, defaults={"username": email})
            profile, profile_created = UserProfile.objects.get_or_create(user=user)

            if profile.remaining_credit != "프리미엄 멤버십":
                try:
                    remaining_credit = int(profile.remaining_credit) if profile.remaining_credit else 0
                    class_credit = class_instance.credit_num

                    if remaining_credit - class_credit < 0:
                        return HttpResponse("""
                            <script type="text/javascript">
                                if (confirm("크레딧이 부족합니다. 구매하러 가시겠습니까?")) {
                                    window.location.href = '/myPage/membership/';
                                } else {
                                    window.history.back();
                                }
                            </script>
                        """)

                    existing_using_credit = int(profile.using_credit) if profile.using_credit else 0
                    new_using_credit = existing_using_credit + class_credit
                    profile.using_credit = str(new_using_credit)
                    profile.remaining_credit = str(remaining_credit - class_credit)
                    profile.save()

                except ValueError:
                    return HttpResponse("잘못된 크레딧 값입니다.", status=400)

            # 전화번호 업데이트
            profile.phone_number = phone
            profile.save()

            # 정원이 다 찼는지 확인
            if class_instance.current_people >= class_instance.capacity:
                # 대기 명단에 추가하는 로직
                return HttpResponse(f"""
                    <script type="text/javascript">
                        if (confirm("수업이 모두 찼습니다. 대기하시겠습니까?")) {{
                            window.location.href = '/mainPage/waiting_list/?classId={class_id}&userId={user.id}';
                        }} else {{
                            window.history.back();
                        }}
                    </script>
                """)

            else:
                class_instance.current_people += 1
                class_instance.save()  # 수업 인원 업데이트

                reservation = Reservation(
                    user_id=user,
                    class_id=class_instance,
                    is_expired=False,
                    center_image_url=center_image_url,
                    center_name=center_name,
                    teacher=class_instance.teacher,
                    date=class_instance.date,
                    time=class_instance.time
                )
                reservation.save()

                return HttpResponse("""
                    <script type="text/javascript">
                        alert("예약이 완료되었습니다.");
                        window.location.href = '/mainPage/';
                    </script>
                """)

    context = {
        'class_instance': class_instance,
        'center_name': center_name,
        'name': request.POST.get('name', ''),
        'phone': request.POST.get('phone', ''),
        'email': request.POST.get('email', ''),
    }
    return render(request, 'reservation_form.html', context)


def add_to_waiting_list(request):
    class_id = request.GET.get('classId')
    user_id = request.GET.get('userId')

    # 수업과 유저 객체를 가져옴
    class_instance = get_object_or_404(Class, id=class_id)
    user = get_object_or_404(User, id=user_id)

    # waiting_people 필드가 문자열로 저장되어 있는지 확인
    waiting_list = str(class_instance.waiting_people).split(',') if class_instance.waiting_people else []

    # 유저가 이미 대기 명단에 있는지 확인 후 추가
    if str(user.id) not in waiting_list:
        waiting_list.append(str(user.id))
        class_instance.waiting_people = ','.join(waiting_list)
        class_instance.save()  # 수업 객체 저장

    # 대기 명단 추가 후 메인 페이지로 리다이렉트
    return HttpResponseRedirect('/mainPage/')


def review_list(request, center_id):
    reviews = Review.objects.filter(class_id__center_data_id=center_id).select_related('class_id', 'user_id')

    review_data = [{
        'user_name': review.user_id.username,
        'teacher': review.class_id.teacher,
        'detail': review.detail,
        'star': review.star,
        'keyword': review.keyword
    } for review in reviews]

    return JsonResponse(review_data, safe=False)


# 마이페이지로 이동
def myPage(request):
    return render(request, 'myPage.html')


# 멤버쉽 페이지로 이동
def membership(request):
    return render(request, 'membership.html')

