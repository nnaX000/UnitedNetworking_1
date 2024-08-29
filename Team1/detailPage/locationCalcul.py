import pandas as pd
import requests

# CSV 파일 경로
csv_file_path = '../yongsan.csv'

# 카카오 API 키
kakao_api_key = "YOUR_KAKAO_API_KEY"

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
    return None, None

# CSV 파일 읽기
df = pd.read_csv(csv_file_path, encoding='cp949')

# 위도와 경도 필드가 이미 있는지 확인
if '위도' not in df.columns or '경도' not in df.columns:
    print("위도와 경도 필드가 없습니다. 주소를 사용해 계산합니다.")
    df['위도'], df['경도'] = zip(*df['주소'].apply(get_lat_lng))
else:
    print("위도와 경도 필드가 이미 존재합니다. 기존 데이터를 사용합니다.")

# 위도와 경도가 제대로 계산되었는지 확인
print(df[['센터 이름', '주소', '위도', '경도']])

# 필요 시 수정된 데이터를 저장
df.to_csv('../yongsan.csv', index=False, encoding='utf-8-sig')
