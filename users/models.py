from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.core.validators import RegexValidator    # telefon numarasinin validation'i icin kullanacagiz

# Create your models here.



class User(BaseUser):  # biz app'imizde username'i degil, email'i kullanacagimiz icin model'den degil BaseUser'dan miras aliyoruz. email, Baseuser modelinden geliyor, o yüzden asagiya eklemiyoruz
    phone_regex = RegexValidator(
        regex=r'^\(\d{3}\) \d{3}-\d{4}$',
        message="Phone number must be in the format: (999) 999-9999"
    )  # telefon numaralarinin validation'inini yapacak semamizi olusturduk

    # ÖNEMLI: Biz Java icin olusturulmus bir API dökümantasyonu üzerinden Python'da bir API olusturuyoruz. Fakat bizden istenileni vermemiz gerektigi icin burada API dökümantasyonunda belirtilen yazim standardina uyacagiz, her ne kadar Python'a uymasa da.. Örnegin, python'da api gelistirirken normalde asagidaki ifadeler mesela firstName  olarak degil first_name olarak yaziliyor, buradaki editör de bize hep onu öneriyor... Bunun yanisira, BaseUser'da zaten hazir first_name, vs alanlar var fakat dökümantasyonun bizden istedigi sekilde degiskenler olusturacagiz burada.
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phoneNumber = models.CharField(validators=[phone_regex], max_length=17,)
    address = models.CharField(max_length=200)
    zipCode = models.CharField(max_length=7)
    builtIn = models.BooleanField(default=False)
    roles = models.CharField(max_length=255)
    confirmPassword = models.CharField(max_length=30)
    # confirmPassword alani ile ilgili, user app'ini tamamladiktan sonra su sekilde bir durum oldugunu farkettim:
    # confirmPassword alani sadece kayit esnasinda kullaniliyor, uygulama'da baska hicbir kullanim alani yok
    # dolayisiyla buna veritabaninda, yani model'de yer verilmemeli, onun yerine serializer'da read_only olarak gecici bir alan olusturulmali
    # uygulamanin baska hicbir yerinde kullanilmiyor ve kullanici sifre degistirdiginde confirmPassword dogal olarak degismiyor.

    objects = BaseUserManager()


