from rest_framework import serializers
from .models import Car


# ÖNEMLI: Frontend kodunda araba ekleme islemi su sekilde gerceklesiyor:
# admin bir arac olusturmaya baslarken, önce bir image olusturuyor. image olusturulduktan sonra,
# image'in id'si ile araci olusturuyor.
# image'i degistirmek istediginde islem update seklinde degil, su sekilde oluyor: image'i siliyor, yeni bir image olusturuyor
# ve bu yeni image'in id'sini söz konusu aracin image id'sine isliyor.
# frontend'in tasarladigi bu sistemde image car ile bir foreign key üzerinden iliskilendirilmiyor, dolayisiyla. biz bu iliskiyi manuel olarak yapacagiz.

class CarSerializer(serializers.ModelSerializer):
    image = serializers.CharField(read_only=True)  # image adinda yeni bir alan olusturduk

    class Meta:
        model = Car
        fields = ('id', 'model', 'doors', 'seats', 'luggage', 'transmission', 'airConditioning',
                  'age', 'pricePerHour', 'fuelType', 'builtIn', 'image',)

    def create(self, validated_data):  #  Bu metot, yeni bir nesne oluşturulduğunda çağrılır. Bu durumda, bir Car nesnesi oluşturulurken kullanılır.
        image_id = self.context['view'].kwargs.get('imageId')  #image_id'yi adres cubugundaki imageId'den aliyoruz - self.context içinden görünümün (view) kwargs'ına erişir ve 'imageId' anahtarını kullanarak image_id'yi aldik.
        validated_data['image'] = image_id
        return super().create(validated_data)

    def to_representation(self, instance):  # Bu metot, bir nesnenin temsilini (representation) oluşturmak için çağrılır.
        representation = super().to_representation(instance)  # üst sınıfın to_representation metodu çağrılır ve nesnenin temsili alınır.
        image = representation.get('image')  # Temsilde 'image' alanını alır.
        if image:
            representation['image'] = [image]  # image'i array icine aldik. cünkü frontend bizden array icerisinde göndermemizi istiyor.
        else:
            representation['image'] = []  # eger image yok ise, bos bir array gönder
        return representation



