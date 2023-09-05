from django.db import models
from cars.models import Car
from users.models import User
from django.utils import timezone


# dokümantasyonda bizden istenen reservation modeli:
# {
#   "id": 0,
#   "car": {
#     "id": 0,
#     "model": "string",
#     "doors": 0,
#     "seats": 0,
#     "luggage": 0,
#     "transmission": "string",
#     "airConditioning": true,
#     "age": 0,
#     "pricePerHour": 0,
#     "fuelType": "string",
#     "builtIn": true,
#     "image": [
#       "string"
#     ]
#   },
#   "userId": 0,
#   "pickUpTime": "2023-09-05T13:18:13.174Z",
#   "dropOffTime": "2023-09-05T13:18:13.174Z",
#   "pickUpLocation": "string",
#   "dropOffLocation": "string",
#   "status": "CREATED",
#   "totalPrice": 0
# }

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    pickUpTime = models.DateTimeField(default=timezone.now())
    dropOffTime = models.DateTimeField(default=timezone.now())
    pickUpLocation = models.CharField(max_length=100)
    dropOffLocation = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='CREATED')
    totalPrice = models.DecimalField(max_digits=20, decimal_places=2)
