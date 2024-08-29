from django.urls import path
from . import views

urlpatterns = [
    #메인페이지로딩
    path('',views.detailPage,name='detailPage'),
    #지역,운동종류에 맞게 검색하기
    path('center_detail/', views.center_detail, name='center_detail'),
]