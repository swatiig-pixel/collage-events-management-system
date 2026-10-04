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
      name="logout",
    ),
    
]
