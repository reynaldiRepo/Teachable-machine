from django.urls import re_path
from teachapp.consumer import TestingConsumer

websocket_urlpatterns = [
    re_path(r'ws/testing/(?P<room_name>\w+)/$', TestingConsumer.as_asgi()),
]