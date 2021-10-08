import core.models as core_models
import core.forms as core_forms
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = "index.html"


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class SignUpView(CreateView):
    form_class = core_forms.CelebrantSignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        celebrant = core_models.Celebrant(user, birthday=form.cleaned_data['birthday'])
        celebrant.save()

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')

        return super().get(*args, **kwargs)
