from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("birthday-wish", views.send_birtday_wish, name="send-birthday-wish")
]
