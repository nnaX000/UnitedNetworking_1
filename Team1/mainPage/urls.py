from django.urls import path
from . import views

urlpatterns = [
    #메인페이지로딩
    path('',views.mainPage,name='mainPage'),
    #지역,운동종류에 맞게 검색하기
    path('filter_centers/', views.filter_centers, name='filter_centers'),
    #센터 클릭하면 상세페이지로 넘어가기
    path('center/<int:center_id>/', views.center_detail, name='center_detail'),
    #센터별 스케줄 불러오기
    path('get_schedule/<int:center_id>/', views.get_schedule, name='get_schedule'),
    #예약 저장
    path('reservation/', views.reservation_view, name='reservation_form'),
    #수업 다 찼을 경우 대기명단에 추가하기
    path('waiting_list/', views.add_to_waiting_list, name='waiting_list'),
]
