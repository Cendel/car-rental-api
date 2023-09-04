from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from .models import Message
from .serializers import MessageSerializer
from rest_framework.response import Response
import math

# Create your views here.


class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):  # bu class'da üc ayri url'yi karsiliyoruz. bu url'ler icin ayri ayri view acmak yerine, bu fonksiyonla bu url'leri karsilayarak tek bir yerde birlestirmis oluyoruz
        if self.request.path == "/contactmessage/request/" or self.request.path == "/contactmessage/request":
            return Message.objects.filter(pk=self.request.query_params.get('id'))
        # return all messages
        return Message.objects.all()

    def list(self, request, *args, **kwargs):
        if request.path.startswith('/contactmessage/pages/') or request.path.startswith('/contactmessage/pages'):
            # bu blok pagination islemi yapiyor. Biz users app'inde de ayni pagination islemi kullanimistik.
            # Aslinda bu fonksiyonu ayri bir sayfada bir modül olarak yazip istedigimiz yerlerde alip kullansaydik daha iyi olurdu.

            # Get the query parameters from the request
            page = request.query_params.get('page', 1)
            size = request.query_params.get('size', 10)
            sort = request.query_params.get('sort', 'id')
            direction = request.query_params.get('direction', 'asc')

            # Convert the query parameters to the appropriate types
            page = int(page)
            size = int(size)
            if page < 1:
                page = 1
            if size < 1:
                size = 1
            # Determine the starting and ending indices for the page
            start_index = (page - 1) * size
            end_index = (start_index + size)

            # Retrieve the Messages according to the requested sort and direction
            if direction.lower() == 'asc':
                try:
                    Messages = Message.objects.order_by(sort)[start_index:end_index]
                except:
                    Messages = Message.objects.order_by(sort)[start_index]

            else:
                try:
                    Messages = Message.objects.order_by(f'-{sort}')[start_index:end_index]
                except:
                    Messages = Message.objects.order_by(f'-{sort}')[start_index]

            # Serialize the Messages and return the response

            serializer = self.serializer_class(Messages, many=True, context={"request": request}, *args, **kwargs)
            total_Messages = Message.objects.count()
            total_pages = math.ceil(total_Messages / size)
            num_elements = len(Messages)
            data = {
                "totalPages": total_pages,
                "totalElements": total_Messages,
                "first": start_index + 1,
                "last": num_elements,
                "number": num_elements,
                "sort": {
                    "sorted": True,
                    "unsorted": False,
                    "empty": False
                },
                "numberOfElements": num_elements,
                "pageable": {
                    "sort": {
                        "sorted": True,
                        "unsorted": False,
                        "empty": False
                    },
                    "pageNumber": page,
                    "pageSize": size,
                    "paged": True,
                    "unpaged": False,
                    "offset": start_index
                },
                "size": size,
                "content": serializer.data,
                "empty": len(serializer.data) == 0,
            }

            return Response(data)
        return super().list(request, *args, **kwargs)

class MessageDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Message.objects.all()
    serializer_class=MessageSerializer
