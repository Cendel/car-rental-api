from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import ImageSerializer
from rest_framework.response import Response

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





