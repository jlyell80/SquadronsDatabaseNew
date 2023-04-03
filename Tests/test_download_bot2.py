from src.DiscordBots.get_screenshot_data_from_discord import ScreenshotCollector, process_message
from src.Database.db_utils import connect_to_mongo
import os


db_name = "SEFDatabase"
mongo_connection_string = f"mongodb+srv://Admin:{os.getenv('MONGO_PW')}@cluster0.jgdzg.mongodb.net/{db_name}?retryWrites=true&w=majority"
connect_to_mongo(mongo_connection_string, db_name)
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = 1015967860918591530
target_width, target_height = 640, 480  # Define the desired resolution for resizing images

client = ScreenshotCollector(CHANNEL_ID, target_height)
client.run(TOKEN)
