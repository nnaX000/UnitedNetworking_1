import pandas as pd
import requests

# CSV 파일 경로
csv_file_path = '../yongsan.csv'

# .env 파일 로드
env = environ.Env()
environ.Env.read_env()

# 카카오 API 키
kakao_api_key = env('KAKAO_API_REST_KEY')

def get_lat_lng(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    params = {"query": address}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if len(result['documents']) > 0:
            lat = result['documents'][0]['y']
            lng = result['documents'][0]['x']
            return lat, lng
    else:
        return None, None

# CSV 파일 읽기
df = pd.read_csv(csv_file_path, encoding='cp949')

# 위도와 경도 필드가 이미 있는지 확인
if '위도' not in df.columns or '경도' not in df.columns:
    df['위도'], df['경도'] = zip(*df['주소'].apply(get_lat_lng))


# 필요 시 수정된 데이터를 저장
df.to_csv('../yongsan.csv', index=False, encoding='utf-8-sig')
