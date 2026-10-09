from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import SignUpForm, LoginForm

urlpatterns = [
    path("signup/",views.signup,name="signup"),
    path("login/",auth_views.LoginView.as_view(
      template_name="accounts/login.html",
      authentication_form=LoginForm,
    ),name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
    path(
      "forgot-password/",
      auth_views.PasswordResetView.as_view(
          template_name="registration/forgot_password.html"
      ),
      name="password_reset"
  ),
  path(
      "reset/<uidb64>/<token>/",
      auth_views.PasswordResetConfirmView.as_view(
          template_name="registration/forgot_password_confirm.html"
      ),
      name="password_reset_confirm"
  ),
  path(
      "forgot-password/done/",
      auth_views.PasswordResetDoneView.as_view(
          template_name="registration/forgot_password_done.html"
      ),
      name="password_reset_done"
  ),
  path(
      "reset/done/",
      auth_views.PasswordResetCompleteView.as_view(
          template_name="registration/forgot_password_complete.html"
      ),
      name="password_reset_complete"
  ),
    
]
