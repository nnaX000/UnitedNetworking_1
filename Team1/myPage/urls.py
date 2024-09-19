from django.urls import path

from . import views

urlpatterns = [
    path('', views.myPage, name='myPage'),
    path('update_alert/', views.update_alert, name='update_alert'),
    path('my_reservation/', views.my_reservation, name='my_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('write_review/<int:reservation_id>/', views.write_review, name='write_review'),
    path('membership/', views.membership, name='membership'),
    path('purchase_membership/', views.purchase_membership, name='purchase_membership'),
    path('membership/purchase/<str:product>/', views.membership_purchase, name='membership_purchase'),
]