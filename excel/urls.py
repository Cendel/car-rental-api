from django.urls import path
from .views import export_user, export_excel_cars, export_excel_reservations

urlpatterns = [
    path('download/users/', export_user, name='users-excel' ),
    path('download/cars/', export_excel_cars, name='excel-cars'),
    path('download/reservations/', export_excel_reservations, name='excel-cars'),
]