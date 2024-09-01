from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='signInUp_profile')
    alert = models.BooleanField(default=False)
    using_credit = models.IntegerField(default=0)
    remaining_credit = models.IntegerField(default=0)
    credit_period = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}의 프로필'
