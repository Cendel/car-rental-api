import math
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from .models import Car
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status


class CarrAddView(CreateAPIView):  # car create view
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Car created successfully", "success": True})


class CarDetailGetView(RetrieveAPIView): # car show by id
    queryset=Car.objects.all()
    serializer_class = CarSerializer


class CarlistView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def list(self, request, *args, **kwargs):
        if request.path.startswith('/car/visitors/pages/') or request.path.startswith('/car/visitors/pages'):
            # take the fields from parameters
            page = request.query_params.get('page', 1)
            size = request.query_params.get('size', 10)
            sort = request.query_params.get('sort', 'id')
            direction = request.query_params.get('direction', 'asc')

            # check the page and size if they are low than 1 and set to 1
            page = int(page)
            size = int(size)
            if page < 1:
                page = 1
            if size < 1:
                size = 1

            # compute the start index and end index to order objects from start to end
            start_index = (page - 1) * size
            end_index = (start_index + size)

            # decide whether objects ordered by direct order or reverse order
            if direction.lower() == 'asc':
                try:
                    Cars = Car.objects.order_by(sort)[start_index:end_index]
                except:
                    Cars = Car.objects.order_by(sort)[start_index]
            else:
                try:
                    Cars = Car.objects.order_by(f'-{sort}')[start_index:end_index]
                except:
                    Cars = Car.objects.order_by(f'-{sort}')[start_index]

            serializer = self.serializer_class(Cars, many=True, context={"request": request}, *args, **kwargs)
            total_Messages = Car.objects.count()
            total_pages = math.ceil(total_Messages / size)
            num_elements = len(Cars)
            data = {
                "totalPages": total_pages,
                "totalElements": total_Messages,
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


class CarDeleteView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Car deleteted successfully", "success": True})


class CarUpdateView(generics.UpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def update(self, request, *args, **kwargs):
        car_id = request.query_params.get('id')
        image_id = request.query_params.get('imageId')
        # frontend'de bize update istegi gönderilirken, url'ye araba id'si ile image id'si ekleliyorlar. biz de yukaridaki iki satirdaki kodda bu id'leri url'den aldik. frontend kodu su sekilde: put(`${API_URL}/car/admin/auth?id=${vehicleId}&imageId=${imageId}`, payload, services.authHeader())

        if not car_id:
            return Response({'detail': 'Car id not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:  # Django'da get metodunu kullanarak veritabanından bir nesne alırken, eşleşen bir nesne bulunamazsa DoesNotExist istisnasını fırlatır.
            return Response({'detail': 'Car not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save(image=image_id)
            return Response({"message": "Car updated successfully", "success": True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# CarUpdateView'i hoca, APIView ile yazmisti (asagidaki kod), generics ile url'deki sorgu parametreleri alinmadigini gerekce göstererek.
# fakat yukarida generics ile denedim, calisiyor...


# class CarUpdateView(APIView):
#     def put(self, request, *args, **kwargs):
#         car_id = request.query_params.get('id')
#         image_id = request.query_params.get('imageId')
#         # frontend'de bize update istegi gönderilirken, url'ye araba id'si ile image id'si ekleliyorlar. biz de yukaridaki iki satirdaki kodda bu id'leri url'den aldik. frontend kodu su sekilde: put(`${API_URL}/car/admin/auth?id=${vehicleId}&imageId=${imageId}`, payload, services.authHeader())
#
#         try:
#             car = Car.objects.get(id=car_id)
#         except Car.DoesNotExist:  # Django'da get metodunu kullanarak veritabanından bir nesne alırken, eşleşen bir nesne bulunamazsa DoesNotExist istisnasını fırlatır.
#             return Response({'detail': 'Car not found.'}, status=404)
#
#         serializer = CarSerializer(car, data=request.data)
#         if serializer.is_valid():
#             serializer.save(image=image_id)
#             return Response({"message": "Car updated successfully", "success": True})
#         return Response(serializer.errors, status=400)