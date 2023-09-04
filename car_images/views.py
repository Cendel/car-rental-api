import mimetypes
import os
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import ImageSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from core import settings
from rest_framework.decorators import api_view

# Create your views here.


class UploadFileView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)  # Django REST framework ile dosya yüklemesi yaparken gelen isteği işlemek için kullanılan veri ayrıştırıcıları (parsers) tanımlar. Bu parsers, gelen isteği istemcinin veri formatına göre doğru şekilde ayrıştırmaya yardımcı olur.
    # MultiPartParser: Bu parser, çoklu parçalı (multipart) form verilerini işlemek için kullanılır. Genellikle dosya yüklemesi için kullanılır. İsteği incelediğinde, birden çok parçadan oluşan veriyi çözümleyerek içeriği ve dosyaları ayırır.
    # FormParser: Bu parser, normal form verilerini işlemek için kullanılır. Form verileri URL kodlamasına (application/x-www-form-urlencoded) veya JSON verilerine benzer bir şekilde ayrıştırılır.
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)  # Gelen istek verilerini ImageSerializer ile işler.
        if file_serializer.is_valid():
            file_serializer.save()
            return Response({  # dökümantasyonun bizden istedigi sekild Response'u düzenliyoruz.
                            'message':'Image upload success',
                            'success': True,
                            "imageId": str(file_serializer.data['id'])
                            },status=201)
        else:
            return Response(file_serializer.errors, status=400)

class ListAllFilesView(ListAPIView):
    queryset= Image.objects.all()
    serializer_class=ImageSerializer


def download_file(request, image_id):  # hocanin aciklamasi: burada django'nun HttpResponse'unu kullanarak image'i indirilebilir olarak gönderiyoruz, burada serializer'lik bir is yok. dosya isteniyor ve gönderiliyor. (burasi bir fonksiyon yerine, RetrieveAPIView olarak yazilabilir mi, arastirilabilir. Ben biraz denedim, olmadi. sanirim gerekmiyor da
    try:  # Bir try bloğu başlar, çünkü medya dosyasının mevcut olup olmadığını kontrol edeceğiz.
        file = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        raise Http404

    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image))  # Medya dosyasının tam yolunu file_path değişkenine oluştururuz. Bu yol, medya dosyasının fiziksel konumunu belirtir. settings.MEDIA_ROOT, medya dosyalarının depolandığı dizini temsil eder.
    if not os.path.exists(file_path):
        raise Http404

    with open(file_path, 'rb') as file_content:  # open: open fonksiyonu, bir dosyanın belirtilen modda (okuma, yazma, vb.) açılmasını sağlar. Bu işlev, dosya işlemleri yaparken kullanılır. file_path: file_path, dosyanın tam yolunu içeren bir dizin yolunu temsil eder. Bu, okumak istediğiniz dosyanın nerede bulunduğunu belirtir. 'rb': İkinci argüman olan 'rb', dosyanın "binary read" modunda açılmasını ifade eder. Bu, dosyanın ikili veriler içerdiğini ve metin dosyası gibi değil, doğrudan ikili verileri okuyacağınızı belirtir. Genellikle resimler, ses dosyaları veya diğer ikili dosyaları okumak için kullanılır. as file_content: Dosya açma işlemi sonucunda elde edilen dosya nesnesini (file_content) belirtilen isimle kullanabilirsiniz. Bu nesne, dosyadaki verilere erişmenizi ve okumanızı sağlar.
        response = HttpResponse(file_content.read(), content_type='application/octet-stream')  # Medya dosyasının içeriğini okuyarak bir HTTP yanıtı oluştururuz. content_type ile yanıtın içeriğinin türünü belirtiriz. Burada application/octet-stream genel bir ikili veri türünü temsil eder.
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)  # İndirme işlemi sırasında tarayıcıda görünen dosya adını ayarlarız. Bu, kullanıcının indirilen dosyanın adını görmesini sağlar.

        return response


def display_image(request, image_id):
    file = get_object_or_404(Image, id=image_id)  # # İstekle gelen image_id'ye sahip Image model nesnesini al veya 404 hatası döndür

    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image))

    if not os.path.exists(file_path):
        raise Http404

    _, file_ext = os.path.splitext(file_path)  # Bu satır, os.path.splitext işlevini kullanarak file_path değişkeninden dosya uzantısını ayıklar. os.path.splitext işlevi, dosya yolunu alır ve dosya adı ile dosya uzantısını içeren bir tuple döndürür. İlk eleman dosya adını, ikinci eleman ise dosya uzantısını içerir. Bu satırda, ilk eleman (_ olarak adlandırılmış, çünkü bu değere ihtiyacımız yok) yok sayılırken, ikinci eleman file_ext değişkenine atanır. Örneğin, eğer file_path "image.jpg" ise, file_ext "jpg" değerini alır.

    content_type, _ = mimetypes.guess_type(file_ext)  # Bu satır, mimetypes.guess_type işlemini kullanarak file_ext değişkeninden MIME türünü tahmin eder. mimetypes.guess_type işlevi, dosya uzantısına dayalı olarak bir dosyanın MIME türünü döndürür. Bu satırda, content_type değişkeni tahmin edilen MIME türünü içerirken, _ olarak adlandırılan ikinci değer yok sayılır. Örneğin, eğer file_ext "jpg" ise, content_type "image/jpeg" değerini alır. Bu MIME türü, tarayıcıya sunulan dosyanın türünü belirtir.
    with open(file_path, 'rb') as file_content:
        response = HttpResponse(file_content, content_type='image/jpeg')  # hoca burada content_type'i jpeg olarak belirlemis, dosyanin türüne göre otomatik ayarlama denemis fakat basaramamis... content_type'i istedigimiz gibi ayarlayabiliyoruz
    return response


@api_view(['DELETE'])  # bu dekoratör ile bize bir delete arayüzü aciyor. bu olmadan da siliyor fakat baska bir hata verir mi emin degilim.
def delete_file(request, image_id):
    file = get_object_or_404(Image, id=image_id)  # Verilen image_id ile Image model nesnesini al veya 404 hatası döndür

    file_path = os.path.join(settings.MEDIA_ROOT, str(file.image))

    if not os.path.exists(file_path):
        raise Http404
    os.remove(file_path)  # dosya yolu belirtilen dosyanin sistemden sildik
    file.delete()  # veritabanindan (objeyi) sildik

    response = Response({'message': 'File and instance deleted succesfully'})
    return response





