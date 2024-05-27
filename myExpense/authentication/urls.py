from django.urls import path
from .views import (
    RegistrationView,
    UservalidationView,
    EmailvalidationView,
    UserLoginView,
    UserLogoutView,
    UserResetPassword,
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # django always checks for cross site forgery so we add csrf_exempt to let other sites send reuest to this url
    path(
        "validateUsername",
        csrf_exempt(UservalidationView.as_view()),
        name="validateUsername",
    ),
    path(
        "validateEmail",
        csrf_exempt(EmailvalidationView.as_view()),
        name="validateEmail",
    ),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("userlogin/", UserLoginView.as_view(), name="login"),
    path("userlogout", UserLogoutView.as_view(), name="logout"),
    path("resetPassword", UserResetPassword.as_view(), name="resetPassword"),
]
