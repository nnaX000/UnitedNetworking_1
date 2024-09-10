from django.contrib import admin
from .models import UserProfile, Reservation, Class, Review

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert', 'using_credit', 'remaining_credit', 'credit_period', 'phone_number')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'class_id', 'center_name', 'teacher', 'date', 'time')
    list_filter = ('user_id', 'class_id', 'date', 'time')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Reservation, ReservationAdmin)
