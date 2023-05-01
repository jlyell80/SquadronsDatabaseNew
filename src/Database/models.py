from mongoengine import *
from datetime import datetime

class Screenshot(Document):
    message_id = StringField(required=True)
    message_data = DictField()
    image_url = StringField()
    image_id = IntField(required=True)
    image_data = BinaryField()
    game_id = ObjectIdField()
    date_added = DateTimeField()
    date_modified = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.date_modified = datetime.utcnow()
        super(Screenshot, self).save(*args, **kwargs)

class Channel(Document):
    channel_id = StringField(required=True, unique=True)
    channel_name = StringField(required=True)
    category_name = StringField(required=True)
    server_name = StringField(required=True)
    date_added = DateTimeField(default=datetime.utcnow)
    date_modified = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.date_modified = datetime.utcnow()
        super(Channel, self).save(*args, **kwargs)