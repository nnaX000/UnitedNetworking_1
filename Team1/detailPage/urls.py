from django.urls import path
from . import views

urlpatterns = [
    #상세페이지로딩
    path('',views.detailPage,name='detailPage'),
]