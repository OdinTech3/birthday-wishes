from django.db import models
from django.contrib.auth.models import User


canbe_blank = {"null": True, "blank": True}
cantbe_blank = {"null": False, "blank": False}


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)


class Celebrant(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(**cantbe_blank)
    about = models.TextField(**canbe_blank)
    avatar = models.ImageField(**canbe_blank)


class Friend(BaseModel):
    first_name = models.CharField(max_length=150, **cantbe_blank)
    last_name = models.CharField(max_length=150, **cantbe_blank)


class BirthdayWish(BaseModel):
    bday_celebrant = models.ForeignKey(
        Celebrant, related_name="birthay_wish", on_delete=models.DO_NOTHING
    )
    well_wisher = models.ForeignKey(Friend, related_name="birthay_wish", on_delete=models.CASCADE)
    text = models.TextField(**cantbe_blank)
