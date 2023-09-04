from django.urls import path
from .views import CarrAddView

urlpatterns = [
    path('admin/<int:imageId>/add/', CarrAddView.as_view(), name='car_add'),  # adding car url
]