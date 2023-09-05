from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservationsViewSet

router = DefaultRouter()
router.register(r'crud', ReservationsViewSet, basename="resevationviewset")

urlpatterns = [
    path('', include(router.urls)),
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
