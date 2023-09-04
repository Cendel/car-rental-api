from django.urls import path
from .views import MessageCreateView,MessageListView,MessageDetailView
urlpatterns = [
    path('visitors/', MessageCreateView.as_view(), name='create_message'),
    path('', MessageListView.as_view(), name='list_all_messages'),
    path('request/', MessageListView.as_view(), name='list_request_message'),  # bu bos bos bir liste döndürüyor, ne icin kullanildigini anlamadim. muhtemelen query parametresi istiyordur...
    path('pages/', MessageListView.as_view(), name='message_list_pages'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail_udg'),
]