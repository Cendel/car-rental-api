from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationsViewSet, ReservationCreateAPIView, ReservationAvailabilityAPIView, ReservationDetailView, ReservationsListAll, ReservationsDeleteView, ReservationUpdateView

router = DefaultRouter()
router.register(r'crud', ReservationsViewSet, basename='reservationviewset')

urlpatterns = [
    path('', include(router.urls)),
    path('add/auth/', ReservationCreateAPIView.as_view(), name='car-user-add-reserv'),  # http://127.0.0.1:8000/reservations/add/?userId=1&carId=3
    path('add/', ReservationCreateAPIView.as_view(), name='car-add-reserv'),
    path('auth/', ReservationAvailabilityAPIView.as_view(), name='reserv-availability'),
    path('<int:pk>/auth/', ReservationDetailView.as_view(), name='reserv-detail-auth'),
    path('<int:pk>/admin/', ReservationDetailView.as_view(), name='reserv-detail-admin'),
    path('admin/all/', ReservationsListAll.as_view(), name='list-admin-all'),
    path('auth/all/', ReservationsListAll.as_view(), name='list-auth'),
    path('admin/auth/all/', ReservationsListAll.as_view(), name='list-auth-admin'),
    path('admin/all/pages/', ReservationsListAll.as_view(), name='list-pages-admin'),
    path('admin/<int:pk>/auth/', ReservationsDeleteView.as_view(), name='delete-reserv'),
    path('admin/auth/', ReservationUpdateView.as_view(), name='reserv-update'),
]


# views.py'de belirttigim gibi, ModelViewSet ile test islemi yapmak istiyoruz. Bu test islemi icin
# urls.py dosyamiz su sekilde olmali:


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ReservationsViewSet
#
# router = DefaultRouter()
# router.register(r'crud', ReservationsViewSet, basename="resevationviewset")  # crud diye yazdigimiz yer, url'imizin endpoint'i. herhangi bir ifade olabilir.
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
