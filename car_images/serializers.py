from rest_framework import serializers
from .models import Image

base_str = "http://127.0.0.1:8000/media/"  # medya dosyalarının temel URL'si. medya dosyalarının sunucuda nasıl erişileceğini belirtir


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()  # serializer sınıfında yeni bir url alanı oluşturduk. Bu alan, asagidaki get_url adlı özel bir metot tarafından doldurulacak.

    class Meta:  # Meta sınıfı, hangi modelin kullanılacağını ve hangi alanların dönüştürüleceğini belirtir.
        model = Image
        fields = ('id', 'name', 'url', 'type', 'size', 'image')  # Dönüştürülen JSON'da hangi alanların yer alacağını belirler. Dökümantasyon'da id belirtilmemisti ama biz ihtiyac olabilecegini düsündük. hoca, aslinda image yerine url'yi kullanabilecegimizi ama her ihtimale karsi imagi i de ekledigini söyledi..

    def get_url(self, obj):  # Bu, url alanını doldurmak için kullanılan özel (custom) bir metottur. Medya dosyasının URL'sini oluşturmak için base_str ile obj.image (resmin adı) birleştirilir.
        url = base_str + "" + str(obj.image)
        return url





