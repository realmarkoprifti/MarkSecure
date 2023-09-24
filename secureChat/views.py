from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import CreateRoomSerializzer, CheckRoomSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Room


# Create your views here.


@api_view(["POST"])
def create_room(request):
    serializer = CreateRoomSerializzer(data=request.data)

    if serializer.is_valid():
        try:
            Room.objects.get(room_id=serializer.validated_data["room_id"])

            return Response({"status": "room_exists"}, HTTP_400_BAD_REQUEST)

        except:
            serializer.save()

            return Response({"status": "room_created"}, HTTP_201_CREATED)

    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def check_room(request):
    serializer = CheckRoomSerializer(data=request.data)

    if serializer.is_valid():
        try:
            Room.objects.get(room_id=serializer.validated_data["room_id"])

            return Response({"status": "room_exists"}, HTTP_200_OK)

        except:
            return Response({"status": "room_valid"}, HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, HTTP_400_BAD_REQUEST)
