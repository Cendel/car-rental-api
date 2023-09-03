from django.urls import path
from .views import RegisterView, LoginView, UserListAPIView, UserDetail, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name = "register"),
    path('login/', LoginView.as_view(), name="register"),
    path('user/', UserListAPIView.as_view(), name="user_personal"),  # tek bir user'in gelip gelmedigini, bu url'nin calisip calismadigini kontrol etmek icin postman gibi bir arac kullanmak gerekiyor. cünkü uygulamanin hangi user'i döndürecegini bilmesi icin token'i da göndermek gerekiyor. bu sekilde user, kendi bilgilerini cekebilir.
    path('user/auth/all/', UserListAPIView.as_view(), name="user_all"),
    path('user/auth/pages/', UserListAPIView.as_view(), name="user_page_all"),  # url'de user/auth/pages?page=1&size=1&sort=id&direction=DESC gibi sorgular yaparak kontrol edebiliriz. bunlar icin api dökümantasyonuna bakabilirsin
    path(('user/<int:pk>/auth/'), UserDetail.as_view(), name='user_detail_auth'),
    path('user/<int:pk>/', UserDetail.as_view(), name="user_detail"),  # bu url aslinda api dökümantasyonunda yer almiyor, hoca her ihtimale karsi bunu ekledi.
    path('user/auth/', ChangePasswordView.as_view(), name="change_password"),  # bu da token istiyor
]