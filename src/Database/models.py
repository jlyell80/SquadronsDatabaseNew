from mongoengine import *


class Screenshot(Document):
    message_id = StringField(required=True)
    message_data = DictField()
    image_url = StringField()
    image_id = IntField(required=True)
    image_data = BinaryField()
    game_id = ObjectIdField()