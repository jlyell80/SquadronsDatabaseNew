from mongoengine import *



def connect_to_mongo(connection_string, db_name):
    connect(host=connection_string)
