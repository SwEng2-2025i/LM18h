import uuid

class User:
    def __init__(self, user_id, name, preferred_channel, channels):
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.preferred_channel = preferred_channel
        self.channels = channels or []
