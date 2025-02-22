from channels.generic.websocket import WebsocketConsumer


class JoinAndLeave(WebsocketConsumer):
    def connect(self):
        self.accept()
        return f"connected"

    def receive(self, text_data=None, bytes_data=None):
        print('client message received in server')
        self.send("Welcome")

    def disconnect(self, code):
        print("disconnected")
