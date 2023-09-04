from django.urls import path
from .views import CarrAddView, CarDetailGetView, CarlistView, CarDeleteView, CarUpdateView

urlpatterns = [
    path('admin/<int:imageId>/add/', CarrAddView.as_view(), name='car_add'),  # adding car url
    path('visitors/<int:pk>/', CarDetailGetView.as_view(), name='car_detail_get'),  # one instance get url for car
    path('visitors/all/', CarlistView.as_view(), name='car_all'),  # list all car url
    path('visitors/pages/', CarlistView.as_view(), name='car_all_pages'),  # list all car with filter # örnek=> http://127.0.0.1:8000/car/visitors/pages/?page=1&size=2&sort=id&direction=DSC
    path('admin/<int:pk>/auth/', CarDeleteView.as_view(), name='car-delete'),  # delete car instance
    path('admin/auth/', CarUpdateView.as_view(), name='car_update')  # updating car instance and image

    # ÖNEMLI: Araci güncellerken image id'sini yazdigimiz image degiskeni disinda her sey normal calisiyor, fakat
    # fakat frontend ve dökümantasyon yapisindan dolayi image id'sini degistirken sunu yapmak gerekiyor:
    # http://127.0.0.1:8000/car/admin/auth/?id=3&imageId=9   => bu url'yi frontend gönderiyor, söyledigi su: id'si 3 olan arabanin image id'sini 9 yapmak istiyorum.
    # dolayisiyla image id'sini degistirmek istedigimizde yeni image id'sini url'ye ekliyoruz ve gönderdigimiz araba bilgilerinde mevcut image id'si yazili kalacak.

]