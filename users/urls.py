from django.urls import path
from .views import RegisterView, LoginView, UserListAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name = "register"),
    path('login/', LoginView.as_view(), name="register"),
    path('user/', UserListAPIView.as_view(), name="user_personal"),
    path('user/auth/all/', UserListAPIView.as_view(), name="user_all"),
    path('user/auth/pages/', UserListAPIView.as_view(), name="user_page_all"),  # url'de user/auth/pages?page=1&size=1&sort=id&direction=DESC gibi sorgular yaparak kontrol edebiliriz. bunlar icin api dökümantasyonuna bakabilirsin
]