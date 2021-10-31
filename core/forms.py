import core.models as models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import localdate
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CelebrantSignUpForm(SignupForm):
    birthday = forms.DateField(
        required=True, label="Birthday", widget=forms.DateInput(attrs={"type": "date"})
    )

    def save(self, request):
        user = super().save(request)

        return user

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']

        if birthday == localdate():
            raise ValidationError("Birthday can not be today!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return birthday


class CelebrantCreationForm(UserCreationForm):
    class Meta:
        model = models.Celebrant
        fields = ("username", "email")


class CelebrantChangeForm(UserChangeForm):
    class Meta:
        model = models.Celebrant
        fields = ("username", "email")
