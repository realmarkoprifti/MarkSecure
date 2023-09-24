from rest_framework import serializers
from .models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        
        
class CreateRoomSerializzer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("room_id", "room_password")
        
        
class CheckRoomSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=200)
    