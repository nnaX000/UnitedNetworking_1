from django.contrib.auth.models import User
from django.db import models

# UserProfile (회원 프로필 관련)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='myPage_profile')
    nickname = models.CharField(max_length=100, blank=True, null=True)  # 닉네임 필드 추가
    alert = models.BooleanField(default=False)
    using_credit = models.CharField(max_length=20, default="0")
    remaining_credit = models.CharField(max_length=20, default="0")
    credit_period = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}의 프로필'
