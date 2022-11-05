from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from user.models import CustomUser
from django.views.generic import View
from user.forms import LoginForm
from django.conf import settings
from . import forms


class LoginPageViews(View):
    form_class = LoginForm
    template_name = "user/login.html"

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
            return redirect("flux")
        message = "Identifiants invalides."
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )


def logout_user(request):
    logout(request)
    return redirect("login")


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "user/signup.html", context={"form": form})
