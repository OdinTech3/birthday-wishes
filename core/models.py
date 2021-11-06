from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse
from uuid import uuid4


canbe_blank = {"null": True, "blank": True}
cantbe_blank = {"null": False, "blank": False}


class BaseModelManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.not_deleted = kwargs.pop("not_deleted", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.not_deleted:
            return BaseModelQuerySet(self.model).filter(deleted_on=None)
        return BaseModelQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModelQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_on=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_on=None)

    def dead(self):
        return self.exclude(deleted_on=None)


class BaseModel(models.Model):
    pkid = models.AutoField(primary_key=True, editable=False)
    _id = models.UUIDField(default=uuid4, editable=False, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(auto_now=False, **canbe_blank)

    objects = BaseModelManager()
    all_objects = BaseModelManager(not_deleted=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_on = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class Celebrant(AbstractUser, BaseModel):
    birthday = models.DateField(**cantbe_blank)
    about = models.TextField(**canbe_blank)
    avatar = models.ImageField(**canbe_blank)

    REQUIRED_FIELDS = ['email', 'birthday']

    def __str__(self):
        return f"{self.first_name} {self.last_name} (🎂 {self.birthday})"

    def get_absolute_url(self):
        return reverse('celebrant', args=[str(self._id)])


class Friend(BaseModel):
    user = models.OneToOneField(Celebrant, to_field="_id", on_delete=models.CASCADE, **canbe_blank)
    first_name = models.CharField(max_length=150, **cantbe_blank)
    last_name = models.CharField(max_length=150, **cantbe_blank)


class BirthdayWish(BaseModel):
    bday_celebrant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        to_field="_id",
        verbose_name='birthday celebrant',
        related_name="birthay_wish",
        on_delete=models.DO_NOTHING,
    )
    well_wisher = models.ForeignKey(
        Friend, to_field="_id", related_name="birthay_wish", on_delete=models.CASCADE
    )
    message = models.TextField(**cantbe_blank)
