from django.urls import path

from . import views

urlpatterns = [
    path('', views.myPage, name='myPage'),
    path('update_alert/', views.update_alert, name='update_alert'),
]