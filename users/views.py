from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from .serializers import RegisterSerializer, CustomLoginSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import math

# Create your views here.


class RegisterView(CreateAPIView):  # ModelViewSets ile yapmamamizin nedeni, bize verilen API dökümantasyonuna uygun olmamasi, frontend ile backend i kendimiz gelistirseydik burada modelviewset i tercih edecektik normalde. api'imizin diger ayarlari da buna göre sekillenecek
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    # Önemli: serializers.py'mizi de yazdik, bu noktada her sey calisiyor. user kayit oluyor ve cevap olarak user'in belirttigimiz bilgileri dönüyor. fakat api dökümantasyonunda bizden user'in bilgilerini döndürmek degil (aslinda alisildik olan bunu yapmak), sadece bir mesaj ve success durumunu döndürmemiz bekleniyor. api dökümantasyona uygun hareket etmek icin, dökümantasyonun istedigini döndürecek aasgida create fonksiyonunu eziyoruz:

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({'message': 'Registeration succesfully done', "success": True})


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer  # Kullanılacak serializer sınıfını belirttik.

    def post(self, request, *args, **kwargs):  # Dökümantasyon bizden, login olundugunda sadece token göndermemizi istiyor, buna göre post fonksiyonunu eziyoruz
        serializer = self.get_serializer(data=request.data)  # İstek verilerini kullanarak serializer oluşturuyoruz.
        serializer.is_valid(raise_exception=True)  # Verilerin geçerli olup olmadığını kontrol ediyoruz, geçerli değilse hata fırlatır.
        user = serializer.validated_data['user']  # # Validation dan gecen kullanıcıyı aliyoruz.
        access_token = str(AccessToken.for_user(user))  # Kullanıcının token ini oluşturuyoruz ve metin formatına çeviriyoruz.

        return Response({'token': access_token})  # yanit olarak token i döndürüyoruz.


# user(lar)imizi listeleyecek class larimizi yaziyoruz:
class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer

    # get_queryset fonksiyonunu, kullanacagimiz queryset'leri duruma göre belirleyecek sekilde eziyoruz:
    def get_queryset(self):
        queryset = User.objects.all() # user'lari aldik

        if self.request.path == '/user/':  # eger tek bir user isteniyorsa (bunu url'deki /user/ ifadesinden anlayacak) belirtilen id'li user'i döndürecek
            return User.objects.filter(id=self.request.user.id)
        else:
            return queryset  # eger if blogu icerisinde dönmediyse, yani tek bir user istenmiyorsa, tüm kullanıcıları içeren queryset'i döndürecek

    # asagida list fonksiyonunu eziyoruz. NOT: get_queryset fonksiyonundan dönen queryset list fonksiyonunda kullanilir. list fonksiyonundaki kod karmasilikligi, dökümantasyonun pagination yapildiginda bizden istedigi verinin karmasik olmasindan kaynakli.
    def list(self, request, *args, **kwargs):
        if request.path.startswith('/user/auth/pages/') or request.path.startswith('/user/auth/pages'):  # eger istegin gönderildigi url pagination istiyorsa buraya girip, pagination islemlerini ve dökümantasyonda belirtilen bilgileri alacak, degilse direkt response'a gececek,
            # Do something if path starts with '/user/auth/pages/'

            # Do something if path starts with '/user/auth/pages'

            # Get the query parameters from the request
            page = request.query_params.get('page', 1)
            size = request.query_params.get('size', 10)
            sort = request.query_params.get('sort', 'id')
            direction = request.query_params.get('direction', 'asc')

            # Convert the query parameters to the appropriate types
            page = int(page)
            size = int(size)
            if page < 1:
                page = 1
            if size < 1:
                size = 1
            # Determine the starting and ending indices for the page
            start_index = (page - 1) * size
            end_index = (start_index + size)

            # Retrieve the users according to the requested sort and direction
            if direction.lower() == 'asc':
                try:
                    users = User.objects.order_by(sort)[start_index:end_index]
                except:
                    users = User.objects.order_by(sort)[start_index]

            else:
                try:
                    users = User.objects.order_by(f'-{sort}')[start_index:end_index]
                except:
                    users = User.objects.order_by(f'-{sort}')[start_index]

            # Serialize the users and return the response

            serializer = self.serializer_class(users, many=True)
            total_users = User.objects.count()
            total_pages = math.ceil(total_users / size)
            num_elements = len(users)
            data = {
                "totalPages": total_pages,
                "totalElements": total_users,
                "first": start_index + 1,
                "last": num_elements,
                "number": num_elements,
                "sort": {
                    "sorted": True,
                    "unsorted": False,
                    "empty": False
                },
                "numberOfElements": num_elements,
                "pageable": {
                    "sort": {
                        "sorted": True,
                        "unsorted": False,
                        "empty": False
                    },
                    "pageNumber": page,
                    "pageSize": size,
                    "paged": True,
                    "unpaged": False,
                    "offset": start_index
                },
                "size": size,
                "content": serializer.data,
                "empty": len(serializer.data) == 0,
            }
            return Response(data)
        return super().list(request, *args, **kwargs)


