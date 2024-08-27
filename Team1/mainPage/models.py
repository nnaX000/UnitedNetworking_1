from django.db import models

# Class(수업 목록 관련)
class Class(models.Model):
    center_data_id = models.IntegerField()
    teacher = models.CharField(max_length=100)
    date = models.CharField(max_length=50)  # 수업 날짜, 문자열로 처리
    time = models.CharField(max_length=50)  # 수업 시작 시간, 문자열로 처리
    duration = models.IntegerField()  # 수업 지속 시간 (분)
    detail = models.CharField(max_length=200)  # 리포매 등 상세 설명
    credit_num = models.IntegerField()  # 크레딧 몇 개인지
    capacity = models.IntegerField()  # 정원
    current_people = models.IntegerField()  # 현재까지 찬 사람
    waiting_people = models.IntegerField()  # 대기하는 사람

    def __str__(self):
        return f"{self.teacher} - {self.date} {self.time}"

# Reservation(회원별 예약 관련)
class Reservation(models.Model):
    user_id = models.IntegerField()  # FK로 설정할 수 있지만, 다른 테이블에서 가져온다고 가정
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_expired = models.BooleanField()  # 지난 수업인지 아닌지

    def __str__(self):
        return f"Reservation for User {self.user_id} - Class {self.class_id}"

# Review(수업별 리뷰 관련)
class Review(models.Model):
    user_id = models.IntegerField()  # FK로 설정할 수 있지만, 다른 테이블에서 가져온다고 가정
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    star = models.IntegerField()  # 별점
    keyword = models.CharField(max_length=100)  # 키워드
    detail = models.TextField()  # 상세 리뷰

    def __str__(self):
        return f"Review by User {self.user_id} for Class {self.class_id} - {self.star} Stars"

