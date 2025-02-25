import json
from tokenize import group

from channels.generic.websocket import WebsocketConsumer

from apps.chat.models import Group


class JoinAndLeave(WebsocketConsumer):
    def connect(self):
        self.accept()
        return f"connected"

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        if type:
            data = text_data.get("data", None)
        if type == "join_group":
            self.join_group(data)
        elif type == "leave_group":
            self.leave_group(data)

    def join_group(self, group_uuid):
        group = Group.objects.get(uuid=group_uuid)
        group.add_user_to_group(self.user)
        data = {
            "type": "join_group",
            "data": group_uuid
        }
        self.send(json.dumps(data))

    def left_group(self, group_uuid):
        group = Group.objects.get(uuid=group_uuid)
        group.remove_user_from_group(self.user)
        data = {
            "type": "leave_group",
            "data": group_uuid
        }
        self.send(json.dumps(data))

    def disconnect(self, code):
        print("disconnected")
