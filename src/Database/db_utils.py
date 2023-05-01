from mongoengine import *
import certifi
ca = certifi.where()

def connect_to_mongo(connection_string):
    return connect(host=connection_string,tlsCAFile=ca)
