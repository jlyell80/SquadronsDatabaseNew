import os
from PIL import Image
from io import BytesIO
from src.Database.db_utils import connect_to_mongo
from src.Database.models import Screenshot

# Define the MongoDB database name and connection string
db_name = "SEFDatabase"
mongo_connection_string = f"mongodb+srv://Admin:{os.getenv('MONGO_PW')}@cluster0.jgdzg.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Connect to the MongoDB database
connect_to_mongo(mongo_connection_string, db_name)

# Retrieve a screenshot document from the database
screenshot_doc = Screenshot.objects.first()

# Print the message data to the console
print(screenshot_doc.image_id)

# Display the screenshot image
image = Image.open(BytesIO(screenshot_doc.image_data))
image.show()
