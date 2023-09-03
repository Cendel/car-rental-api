from django.urls import path
from .views import MessageCreateView
urlpatterns = [
    path('visitors/', MessageCreateView.as_view(), name='create_message'),
]