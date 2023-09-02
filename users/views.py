from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Create your views here.


class RegisterView(CreateAPIView):  # ModelViewSets ile yapmamamizin nedeni, bize verilen API dökümantasyonuna uygun olmamasi, frontend ile backend i kendimiz gelistirseydik burada modelviewset i tercih edecektik normalde. api'imizin diger ayarlari da buna göre sekillenecek
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer