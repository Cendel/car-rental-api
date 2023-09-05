from django.db import models

# dokümantasyonda bizden istenen car modeli:

# {
#   "id": 0,
#   "model": "string",
#   "doors": 0,
#   "seats": 0,
#   "luggage": 0,
#   "transmission": "string",
#   "airConditioning": true,
#   "age": 0,
#   "pricePerHour": 0,
#   "fuelType": "string",
#   "builtIn": true,
#   "image": [
#     "string"
#   ]
# }

TRANSMISSION = (
    ('a', 'Automatic'),  # veritabaninda "a" olarak kayitli olacak, secenek belirtme ekraninda uzun hali görülecek. böylece veritabaninda gereksiz yer kaplamayacak.
    ('m', 'Manual'),
    ('t', 'Tiptronic'),
)

FUEL = (
    ('e', 'Electricity'),
    ('h', 'Hybrid'),
    ('g', 'Gasoline'),
    ('d', 'Diesel'),
    ('a', 'Hydrogen'),
    ('l', 'LPG'),
    ('c', 'CNG'),
)


class Car(models.Model):
    model = models.CharField(max_length=100)
    doors = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField()
    transmission = models.CharField(max_length=5, choices=TRANSMISSION)
    airConditioning = models.BooleanField()
    age = models.PositiveIntegerField()
    pricePerHour = models.DecimalField(max_digits=8, decimal_places=2)
    fuelType = models.CharField(max_length=2, choices=FUEL)
    builtIn = models.BooleanField(default=True)
    image = models.CharField(max_length=30, blank=True, null=True)
