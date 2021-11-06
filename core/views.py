from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required
import core.models as models
import core.forms as forms


def index(request):
    return render(request, "index.html", {"form": forms.BirthDayWishForm()})


@require_POST
def send_birtday_wish(request):
    bday_model = models.BirthdayWish()
    bday_form = forms.BirthDayWishForm(request.POST)

    if bday_form.is_valid():
        data = bday_form.cleaned_data

        if request.user.is_authenticated:
            logged_user = request.user
            friend = models.Friend(
                first_name=logged_user.first_name,
                last_name=logged_user.last_name,
                user=logged_user
            )
            friend.save()
        else:
            friend = models.Friend(
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            friend.save()

        bday_model.bday_celebrant = data["user"]
        bday_model.well_wisher = friend
        bday_model.message = data["message"]
        bday_model.save()

        return redirect(reverse("index"))

    context = {"form": bday_form}

    return render(request, "index.html", context)
