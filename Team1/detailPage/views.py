from django.shortcuts import render

def detailPage(request):
    return render(request, 'detailed_center.html')

def center_detail(request, center_id):
    # CSV 파일 로드
    csv_file_path = '../yongsan.csv'
    df = pd.read_csv(csv_file_path, encoding='cp949')

    # center_id로 해당 센터 데이터 검색
    center_data = df[df['id'] == center_id].iloc[0]
    
    context = {
        'center': {
            'name': center_data['센터 이름'],
            'address': center_data['주소'],
            'phone': center_data['전화번호'],
            'latitude': center_data['위도'],
            'longitude': center_data['경도'],
            'image_url': center_data['사진'],
            'info': center_data['기타 정보'],  # 기타 필요한 정보
        }
    }

    return render(request, 'detailed_center.html', context)

