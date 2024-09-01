from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alert = models.BooleanField(default=False)  # 알림 설정
    using_credit = models.IntegerField(default=0)  # 사용한 크레딧
    remaining_credit = models.IntegerField(default=0)  # 남은 크레딧
    credit_period = models.CharField(max_length=100, blank=True, null=True)  # 크레딧 기간
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 전화번호

    def __str__(self):
        return f'{self.user.username}의 프로필'
