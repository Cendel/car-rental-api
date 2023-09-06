from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from core.page_filter import pages_filter


# serializers.py dosyasinin yazimini tamamen bitirdik. views.py dosyasinin yazimina gecmeden önce veritabanimiz ve
# bu zamana kadar kurdugumuz sistemin calisip calismadigini kontrol etmek istiyoruz. ModelViewSet, veritabani islemlerinin
# testini mümkün kiliyor. CreateAPIView ile de yapabilirdik fakat bu yöntem daha elverisli.
# Bunun icin önce asagida ReservationsViewSet olusturuyoruz. Bunu API'imizda kullanmayacagiz, sadece bu test islemi
# icin olusturduk.
# Daha sonra urls.py dosyasini yaziyoruz. Nasil yazacagimizi o dosyadan takip edebilirsin.

class ReservationsViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# testimizi yaptik, simdi view'lerimizi yazmaya basliyoruz.


class ReservationCreateAPIView(APIView):
    def post(self, request, formal=None):
        user_id = None
        if request.path == '/reservations/add/auth/' or request.path == '/reservations/add/auth':
            user_id = request.query_params.get('userId')
        elif request.user.is_authenticated:
            user_id = request.user.id
        car_id = request.query_params.get('carId')

        if not user_id or not car_id:
            return Response(
                {'error': 'userId and carId are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data.copy()  #  İsteğin verilerini (request.data) bir kopyasını data değişkenine atar. Bu, veriler üzerinde değişiklik yapmak için kullanılabilir.

        data['user_id'] = user_id
        data['car_id'] = car_id
        serializer = ReservationSerializer(data=data)  # serializer = ReservationSerializer(data=data) - ReservationSerializer sınıfı kullanılarak data verileri ile bir seri (serializer) oluşturulur. Bu seri, verilerin doğruluğunu ve uygunluğunu kontrol etmek için kullanılır.

        if serializer.is_valid():
            reservation = serializer.save()
            return Response(
                {'message': 'Reservation created successfully.', "success": True},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ReservationAvailabilityAPIView(APIView):

    def get(self, request, format=None):
        car_id = request.query_params.get('carId')
        pick_up_date_time = request.query_params.get('pickUpDateTime')
        drop_off_date_time = request.query_params.get('dropOffDateTime')

        if not car_id or not pick_up_date_time or not drop_off_date_time:
            return Response(
                {
                    'error': 'carId, pickUpDateTime and dropOffDateTime are required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        reservations = Reservation.objects.filter(
            car_id=car_id,
            dropOffTime__gte=pick_up_date_time,  # Bu koşul, rezervasyonların dropOffTime alanının, belirli bir pick_up_date_time değerinden büyük veya eşit olmasını gerektirir.
            pickUpTime__lte=drop_off_date_time  # Bu koşul, rezervasyonların pickUpTime alanının, belirli bir drop_off_date_time değerinden küçük veya eşit olmasını gerektirir.
        )
        if reservations.exists():
            return Response(
                {
                    'message': 'Car is not available for this time period.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {
                    'message': 'Car is  available for this time period.', 'success': True
                }, status=status.HTTP_200_OK
            )


class ReservationDetailView(RetrieveAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Reservation.objects.none()  # queryset'i önce global olarak (ici bos olacak sekilde) tanimladik. if'li bloklarda lokal problemi olmamasi icin. ayrica, if'li bloklar karsilanmazsa bos bir set döndürmüs olacagiz.
        if not pk:
            raise NotFound("There is no id in the URL")

        if self.request.path.endswith("/auth/"):
            user_id = self.request.user.id   # Django REST framework, isteği yapan kullanıcının kimlik bilgilerini self.request.user üzerinden sağlar. Bu kullanıcı nesnesi, oturum açmış olan kullanıcının kimlik bilgilerini içerir. Bu nesne üzerinden id özelliği kullanılarak kullanıcının kimliği (user_id) elde edilir. Eğer kullanıcı oturum açmış değilse, user_id değeri boş olur ve bu durumda bir PermissionDenied istisnası fırlatılır.
            if not user_id:
                raise PermissionDenied('User is not authenticated')
            queryset = Reservation.objects.filter(user_id=user_id)
            if not queryset:
                raise NotFound("This user does not have any reservations in this id")
            return queryset

        if self.request.path.endswith("/admin/"):
            if self.request.user.is_staff:
                queryset = Reservation.objects.all()
            else:
                raise NotFound("This user is not admin")
            return queryset

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if queryset is None:
                raise NotFound('There is no reservation')
            return super().get(request, *args, **kwargs)
        except (NotFound, PermissionDenied) as e:
            return Response(str(e), status=e.status_code)


class ReservationsListAll(ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if self.request.path == "/reservations/admin/all/" and self.request.user.is_staff:
            return Reservation.objects.all()
        elif self.request.path == "/reservations/admin/all/" and not self.request.user.is_staff:
            return Reservation.objects.none()
        if self.request.user.is_staff:
            return Reservation.objects.all()
        elif self.request.user.is_authenticated:
            return Reservation.objects.filter(user_id=self.request.user.id)
        else:
            return Reservation.objects.none()

    def list(self, request, *args, **kwargs):
        if request.path == "/reservations/auth/all/":  # this end point check authenticated
            # user reservations and list them with filter
            return pages_filter(self, request, Reservation, *args, **kwargs)  # core'da yazdigimiz pages_filter modülü ile pagination yapiyoruz
        elif request.path == "/reservations/admin/auth/all/":
            return pages_filter(self, request, Reservation, *args, **kwargs)
        elif request.path == "/reservations/admin/all/pages/":
            return pages_filter(self, request, Reservation, *args, **kwargs)

        return super().list(request, *args, **kwargs)


class ReservationsDeleteView(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            pk = self.kwargs['pk']
            super().destroy(request, *args, **kwargs)
            return Response({
                'message': f'Reservation-{pk} is deleted succesfully', 'success': True
            })
        return Response({'message': 'Only Admin can delete reservations'}, status=status.HTTP_401_UNAUTHORIZED)


class ReservationUpdateView(APIView):

    def put(self, request, id=None):

        r_id = request.query_params.get('reservationId')
        car_id = request.query_params.get('carId')
        self.kwargs['pk'] = r_id
        if not r_id or not car_id:
            return Response(
                {'error': 'id and carId are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.is_staff:

            data = request.data.copy()

            data['id'] = r_id
            data['car_id'] = car_id
            instance = Reservation.objects.filter(id=r_id).first()
            serializer = ReservationSerializer(instance, data=data, partial=True)

            if serializer.is_valid():
                reservation = serializer.save()
                return Response(
                    {'message': 'Reservation updated successfully.', "success": True},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({
                "message": "Only Admin can update reservations"
            })