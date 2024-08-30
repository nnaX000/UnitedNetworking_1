from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
import logging
from django.template.loader import get_template, TemplateDoesNotExist
import re
import os
from django.conf import settings
from .models import Class 


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(BASE_DIR, 'yongsan.csv')


#메인페이지 로딩
def mainPage(request):
    return render(request, 'mainPage.html')

#지역,운동종류에 맞게 검색하기
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
    results = filtered_df[['id', '센터 이름', '사진']].to_dict('records')

    return JsonResponse(results, safe=False)

    

#특정 체육관 클릭시 상세페이지 넘어가게 하기
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
            'id':center_data['id'],
            'name': center_data['센터 이름'],
            'address': center_data['주소'],
            'phone': center_data['전화번호'],
            'latitude': center_data['위도'],
            'longitude': center_data['경도'],
            'image_url': center_data['사진'],
            'info': center_data['기타 정보'],  # 기타 필요한 정보
        },
        'kakao_api_key': settings.KAKAO_API_JS_KEY,  # API 키를 템플릿으로 전달
    }

    return render(request, 'detailed_center.html', context)

#기관별 스케줄 가져오기
def get_schedule(request, center_id):

    # Fetch all classes associated with the given center_id
    classes = Class.objects.filter(center_data_id=center_id).values(
        'time', 'detail', 'credit_num', 'duration', 'teacher'
    )

    # Convert queryset to list of dictionaries
    classes_list = list(classes)

    return JsonResponse(classes_list, safe=False)



