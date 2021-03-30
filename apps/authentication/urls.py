from django.urls import path, include
from apps.authentication import views
app_name  = "authentication"
urlpatterns = [
    path("token/", views.Token.as_view(), name='login'),
    path("register/", views.Register.as_view(), name='signup'),
    path("otp/resend/", views.ResendOtpView.as_view()),
    path("change/password/", views.ChangePasswordView.as_view()),
    path("forget/password/", views.ForgetPasswordView.as_view()),
    path("update/profile/", views.UpdateProfileView.as_view()),
    # path("token/refresh/", views.RefreshToken.as_view()),
    path("token/revoke/", views.revoke_tokens),
]
