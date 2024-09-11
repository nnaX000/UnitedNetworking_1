from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Class(수업 목록 관련)
class Class(models.Model):
    center_data_id = models.IntegerField()
    teacher = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    duration = models.IntegerField()
    detail = models.CharField(max_length=200)
    credit_num = models.IntegerField()
    capacity = models.IntegerField(default=0)
    current_people = models.IntegerField(default=0)
    waiting_people = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.teacher} - {self.date} {self.time}"

class Reservation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mainPage_reservation')  # FK로 설정할 수 있지만, 다른 테이블에서 가져온다고 가정
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_expired = models.BooleanField()
    center_name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)

    def __str__(self):
        return f"Reservation for User {self.user_id} - Class {self.class_id}"
    
    
    def update_expiration_status(self):
        # 현재 연도 가져오기
        current_year = datetime.now().year
        
        # "9월 20일 18:00" 같은 형식을 처리하기 위한 파싱
        reservation_datetime_str = f"{current_year}년 {self.date} {self.time}"
        
        try:
            # 연도를 포함한 날짜 형식을 파싱 (예: '2024년 9월 20일 18:00')
            reservation_datetime = datetime.strptime(reservation_datetime_str, "%Y년 %m월 %d일 %H:%M")
        except ValueError:
            return  # 잘못된 형식의 경우 에러 처리
        
        # 현재 시각과 비교하여 예약이 만료되었는지 확인
        current_datetime = datetime.now()
        
        if current_datetime > reservation_datetime:
            self.is_expired = True
            self.save()
        else:
            print(f"예약 유지: {reservation_datetime_str}, 현재 시각보다 미래임.")


# Review(수업별 리뷰 관련)
class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mainPage_review')  # username을 email로 설정해놔서
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    star = models.IntegerField()  # 별점
    keyword = models.CharField(max_length=100)  # 키워드
    detail = models.TextField()  # 상세 리뷰

    def __str__(self):
        return f"Review by User {self.user_id} for Class {self.class_id} - {self.star} Stars"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mainPage_profile')
    alert = models.BooleanField(default=False)
    using_credit = models.CharField(max_length=20, default="0")
    remaining_credit = models.CharField(max_length=20, default="0")
    credit_period = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}의 프로필'

