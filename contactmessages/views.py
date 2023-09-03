from rest_framework.generics import CreateAPIView
from .models import Message
from .serializers import MessageSerializer

# Create your views here.


class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
