from django.urls import path
from . import views

urlpatterns = [
    #메인페이지로딩
    path('',views.mainPage,name='mainPage'),
    #지역,운동종류에 맞게 검색하기
    path('filter_centers/', views.filter_centers, name='filter_centers'),
]
