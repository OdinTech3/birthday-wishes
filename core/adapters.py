from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user = super().save_user(request, user, form, commit=False)
        user.birthday = data["birthday"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]

        user.save()

        return user
