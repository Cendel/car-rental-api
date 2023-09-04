from rest_framework.generics import CreateAPIView
from .models import Car
from .serializers import CarSerializer
from rest_framework.response import Response

class CarrAddView(CreateAPIView):  # car create view
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Car created successfully", "success": True})