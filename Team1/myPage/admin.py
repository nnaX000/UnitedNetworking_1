from django.contrib import admin
from mainPage.models import Reservation, Class, Review
from myPage.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'alert', 'using_credit', 'remaining_credit', 'credit_period', 'phone_number')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'class_id', 'center_name', 'teacher', 'date', 'time')
    list_filter = ('user_id', 'class_id', 'date', 'time')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reservation, ReservationAdmin)
