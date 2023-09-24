import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Room, Message
from .serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
            self.password = self.scope["url_route"]["kwargs"]["password"]
            self.room_group_name = f"room_{self.room_id}"
            room = Room.objects.get(room_id=self.room_id)
            messages = room.messages.all().order_by("timestamp")
            
            if room.room_password == self.password:
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name, self.channel_name
                )
                self.accept()
                
                if messages.count() > 0:
                    serializer = MessageSerializer(messages, many=True)

                    for message in serializer.data:
                        self.send(json.dumps(message))
                
            else:
                self.close()
            
        except:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        try:
            json_data = json.loads(text_data)
            message_json = json_data["content"]
            
            message = Message.objects.create(content=message_json)
            message.save()
            
            
            serializer = MessageSerializer(message)

            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {
                    "type": "chat", 
                    "content": serializer.data.get("content"), 
                    "timestamp": serializer.data.get("timestamp")
                }
            )
            
            room = Room.objects.get(room_id=self.room_id)
            room.messages.add(message)
            room.save()
            
        except:
            self.close(500)
            
    def chat(self, event):
        content = event["content"]
        timestamp = event["timestamp"] 
        
        self.send(text_data=json.dumps({
            "content": content,
            "timestamp": timestamp
        }))