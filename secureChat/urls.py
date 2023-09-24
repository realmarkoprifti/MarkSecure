from django.urls import path
from .views import *


urlpatterns = [
    path("api/create/room", create_room, name="create_room"),
    path("api/check/room", check_room, name="check_room"),
]
