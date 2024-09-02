from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert', 'using_credit', 'remaining_credit', 'credit_period', 'phone_number')

# 모델과 Admin 클래스를 admin에 등록
admin.site.register(UserProfile, UserProfileAdmin)
