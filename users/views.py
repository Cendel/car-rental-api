from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from .serializers import RegisterSerializer, CustomLoginSerializer
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.


class RegisterView(CreateAPIView):  # ModelViewSets ile yapmamamizin nedeni, bize verilen API dökümantasyonuna uygun olmamasi, frontend ile backend i kendimiz gelistirseydik burada modelviewset i tercih edecektik normalde. api'imizin diger ayarlari da buna göre sekillenecek
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    # Önemli: serializers.py'mizi de yazdik, bu noktada her sey calisiyor. user kayit oluyor ve cevap olarak user'in belirttigimiz bilgileri dönüyor. fakat api dökümantasyonunda bizden user'in bilgilerini döndürmek degil (aslinda alisildik olan bunu yapmak), sadece bir mesaj ve success durumunu döndürmemiz bekleniyor. api dökümantasyona uygun hareket etmek icin, dökümantasyonun istedigini döndürecek aasgida post fonksiyonunu eziyoruz:

    def post(self, request, *args, **kwargs):
        return Response({'message': 'Registeration succesfully done', "success": True})


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer  # Kullanılacak serializer sınıfını belirttik.

    def post(self, request, *args, **kwargs):  # Dökümantasyon bizden, login olundugunda sadece token göndermemizi istiyor, buna göre post fonksiyonunu eziyoruz
        serializer = self.get_serializer(data=request.data)  # İstek verilerini kullanarak serializer oluşturuyoruz.
        serializer.is_valid(raise_exception=True)  # Verilerin geçerli olup olmadığını kontrol ediyoruz, geçerli değilse hata fırlatır.
        user = serializer.validated_data['user']  # # Validation dan gecen kullanıcıyı aliyoruz.
        access_token = str(AccessToken.for_user(user))  # Kullanıcının token ini oluşturuyoruz ve metin formatına çeviriyoruz.

        return Response({'token': access_token})  # yanit olarak token i döndürüyoruz.
