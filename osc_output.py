
from pythonosc import udp_client

class OSCOutput:
    def __init__(self, ip, port):
        self.client = udp_client.SimpleUDPClient(ip, port)

    def send_position(self, x, y):
        self.client.send_message("/stage/position/x", x)
        self.client.send_message("/stage/position/y", y)
        self.client.send_message("/stage/position", [x, y])

    def send_active(self, active):
        self.client.send_message("/stage/active", 1 if active else 0)
