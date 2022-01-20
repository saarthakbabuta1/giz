from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
        # ex: api/user/register/
    path("register/", views.RegisterView.as_view(), name="Register"),
    # ex: api/user/login/
    path("login/", views.LoginView.as_view(), name="Login"),
    # ex: api/user/isunique/
    path("isunique/", views.CheckUniqueView.as_view(), name="Check Unique"),
        # ex: api/user/account/
    path(
        "account/",
        views.RetrieveUpdateUserAccountView.as_view(),
        name="Retrieve Update Profile",
    ),
        path(
        "refresh-token/", views.CustomTokenRefreshView.as_view(), name="refresh_token"),
        # ex: api/user/otp/
    path("otp/", views.OTPView.as_view(), name="OTP"),
    # ex: api/user/otpreglogin/
    path("otpreglogin/", views.OTPLoginView.as_view(), name="OTP-Register-LogIn")
 ]