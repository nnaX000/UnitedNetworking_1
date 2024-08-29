from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
import logging
from django.template.loader import get_template, TemplateDoesNotExist
import re

logger = logging.getLogger(__name__)
csv_file_path = '../yongsan.csv' 

#메인페이지 로딩
def mainPage(request):
    return render(request, 'mainPage.html')

#지역,운동종류에 맞게 검색하기
def filter_centers(request):
    dong = request.GET.get('dong')
    exercise = request.GET.get('exercise')

    # CSV 파일 로드
    df = pd.read_csv(csv_file_path, encoding='cp949')
    print(df.columns)


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
    results = filtered_df[['센터 이름', '사진']].to_dict('records')

    return JsonResponse(results, safe=False)

