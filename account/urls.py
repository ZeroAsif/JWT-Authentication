from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,PasswordResetView,UserPasswordResetView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password/',PasswordResetView.as_view(), name='send-reset-password'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(), name='reset-password'),
]
