from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):  # kayit islemi icin
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]  # email unique olmali ve bu unique'lik User.objects.all() queryset'i icerisinde aranmali dedik
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])  # password'ü kullaniciya geri döndürmeyecegimiz icin write only dedik
    confirmPassword = serializers.CharField(write_only=True, required=True)  # frontend'de password kontrolü tekrar confirm ediliyor fakat yine de önlem almis oluyoruz

    class Meta:
        model = User
        fields = ('id', 'firstName', 'lastName', 'password', 'confirmPassword', 'address', 'zipCode', 'phoneNumber', 'builtIn', 'roles', 'email')

    def validate(self, attrs):  # validation isleminden gecirecegimiz fonksiyon (ilk password ile ikincisi ayni mi)
        if attrs["password"] != attrs["confirmPassword"]:
            raise serializers.ValidationError({"password:", "Password fields did not match."})
        return attrs

    def create(self, validated_data):  # validated_data'nin nasil kayit edilecegini belirtiyoruz
        user = User.objects.create_user(**validated_data)  # bir use olusturulmasini ve bunun User modeline göre olusturmasini söyledik
        user.set_password(validated_data["password"])  # olusturdugumuz user icin password'ü set ettik, password olarak validated_data'nin password'ünü kullan dedik
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):  # burada authentication islemi yapacagimiz, dolayisiyla burada döndürülecek bir sey olmadigi icin ModelSerializer degil, Serializer kullandik
    # bize kullanicidan bir email ve password gelecek, bunlari karsilamak icin:
    email = serializers.EmailField()
    password = serializers.CharField()

    # validate islemi icin:
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')  # validate edecegimiz degerleri aldik

        if email and password:  # eger bunlar varsa:
            user = authenticate(request=self.context.get('request'), email=email, password=password)  # yukarida import ettigimiz authenticate fonksiyonunu kullandik
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            attrs['user'] = user  # bu noktada user authenticate edildigi icin artik onu deger olarak atadik
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')

        # token'in süresi ve daha bircok ayar icin, simplejwt dökümantasyonunu inceleyebilirsin.


class UserSerializer(serializers.ModelSerializer):
    # ÖNEMLI: API dökümantasyonunda roles variable'i bir liste seklinde fakat SQLite liste, array gibi karmasik veri tiplerini desteklemiyor. Dolayisiyla burada, bizim roles yapimizi SQLite'in kabul edecegi bir formatta yazacagiz. diger degiskenlerde problem olmadigi icin onlari herhangi bir isleme sokmadan modelimizden alacagiz
    # bizim burada roles üzerinde yapacagimiz islem, liste'yi alip string'e cevirecek ve veritabaninda o sekilde tutacak, response gönderilirken de onu veritabanindan alip listeye cevirecek.
    # normalde django icin böyle bir role variable ina ihtiyac yok. dökümantasyon java icin üretildigi ve frontend de java api'yina göre yapildigi icin bunu eklemek zorunda kaldik.
    roles = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=False,
        required=False,
    )

    class Meta:
        model = User
        fields = ('id', 'firstName', 'lastName', 'address', 'zipCode', 'phoneNumber', 'builtIn', 'roles', 'email')

    # response'dan önce, roles degiskenimizi tekrar bir listeye cevirmek icin asagida, serializer'in response gönderen fonksiyonu üzerinde düzenleme yapiyoruz:
    def to_representation(self, instance):
        data = super().to_representation(instance)
        roles_str = data.pop('roles')
        roles_list = "".join(roles_str).replace("[", "").replace("]", "").replace("'", "")
        roles_list = roles_list.split(",")
        data['roles'] = roles_list

        return data



