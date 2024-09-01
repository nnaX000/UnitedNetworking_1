import pandas as pd
import requests
import environ
import os
import django
from django.conf import settings

# CSV 파일 경로
csv_file_path = 'yongsan.csv'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Team1.settings')
django.setup()

kakao_api_key = settings.KAKAO_API_REST_KEY


def get_lat_lng(address):
    # 여기에 주소를 위도와 경도로 변환하는 API 호출 로직이 들어갑니다.
    # 예를 들어, 카카오 API를 사용하여 좌표를 얻는 경우:
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    params = {"query": address}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            lat = result['documents'][0]['y']
            lng = result['documents'][0]['x']
            return float(lat), float(lng)
    
    # 위의 조건이 만족되지 않으면 None을 반환
    return None

# CSV 파일 읽기
df = pd.read_csv(csv_file_path, encoding='cp949')

# 위도와 경도 필드가 이미 있는지 확인
if '위도' not in df.columns or '경도' not in df.columns:
    df['위도'], df['경도'] = zip(*df['주소'].apply(lambda x: get_lat_lng(x) if get_lat_lng(x) is not None else (None, None)))
    
    # None이 있을 경우를 처리
    df.dropna(subset=['위도', '경도'], inplace=True)  # 위도나 경도가 None인 행은 제거



# 필요 시 수정된 데이터를 저장
df.to_csv('yongsan.csv', index=False, encoding='utf-8-sig')
