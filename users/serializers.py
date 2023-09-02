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

