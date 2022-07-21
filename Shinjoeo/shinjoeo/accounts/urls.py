from django.urls import path
from .views import kakaoGetLogin, getUserInfo,logoutView

urlpatterns = [
    path('login/', kakaoGetLogin),
    path('accounts/login/callback/', getUserInfo, name="kakao_callback"),
    path('logout/',logoutView),
]