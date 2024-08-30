from django.urls import path
from . import views

app_name = "signInUp" #namespace 가 signInUp 라는 이름을 가졌음을 명시

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]