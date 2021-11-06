from django.db.models import fields
import core.models as models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import localdate
from allauth.account.forms import SignupForm


class CelebrantSignUpForm(SignupForm):
    birthday = forms.DateField(
        required=True, label="Birthday", widget=forms.DateInput(attrs={"type": "date"})
    )
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    def clean_birthday(self):
        birthday = self.cleaned_data["birthday"]

        if birthday == localdate():
            raise ValidationError("Birthday can not be today!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return birthday


class BirthDayWishForm(forms.Form):
    user = forms.ModelChoiceField(queryset=models.Celebrant.objects.all(), initial=0)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea)
