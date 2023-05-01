from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from src.Database.db_utils import connect_to_mongo
from src.DiscordBots.create_channel_document import create_channel_document
from discord.ext import commands
from discord import Intents
from bson.json_util import dumps, loads
import base64
import threading
import asyncio

app = Flask(__name__)

# Configure the MongoDB connection
db_name = "SEFDatabase"
mongo_connection_string = f"mongodb+srv://Admin:{os.getenv('MONGO_PW')}@cluster0.jgdzg.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Connect to the MongoDB database
db_connection = connect_to_mongo(mongo_connection_string)

def get_db():
    return db_connection[db_name]

@app.route('/')
def home():
    db = get_db()
    collections = []
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        count = collection.count_documents({})
        collections.append({"name": collection_name, "count": count})
    return render_template('index.html', collections=collections)

@app.route('/get_channels')
def get_channels():
    db = get_db()
    channels = db['channel'].find({})
    data = [{"id": str(channel['channel_id']),
             "name": f"{channel['server_name']} - {channel['category_name']} - {channel['channel_name']}" if channel['category_name'] != "No Category" else f"{channel['server_name']} - {channel['channel_name']}"}
            for channel in channels]
    return jsonify(data)


@app.route('/add_discord_channel', methods=['POST'])
def add_discord_channel():
    channel_id = request.json['channel_id']
    async def add_channel():
        try:
            await create_channel_document(discord_client, int(channel_id))
        except Exception as e:
            return f"An error occurred while adding the channel: {e}", 400
        return "Channel added successfully", 200

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(add_channel())
    loop.close()

    return result

@app.route('/view_item/<string:collection_name>/<int:item_index>')
def view_item(collection_name, item_index):
    db = get_db()
    collection = db[collection_name]
    item = collection.find().skip(item_index).limit(1)

    item_data = loads(dumps(item))[0]  # Convert BSON to JSON and then to a Python dictionary

    for key, value in item_data.items():
        if isinstance(value, bytes) and value.startswith(b'\x89PNG'):  # Check if the value is a PNG image
            img_data = base64.b64encode(value).decode('utf-8')
            item_data[key] = f"data:image/png;base64,{img_data}"

    return render_template('item_view.html', item_data=item_data, collection_name=collection_name, item_index=item_index)

@app.route('/view_item/<string:collection_name>/<int:item_index>/next')
def view_next_item(collection_name, item_index):
    item_index += 1
    return redirect(url_for('view_item', collection_name=collection_name, item_index=item_index))

@app.route('/view_item/<string:collection_name>/<int:item_index>/previous')
def view_previous_item(collection_name, item_index):
    item_index = max(item_index - 1, 0)
    return redirect(url_for('view_item', collection_name=collection_name, item_index=item_index))



if __name__ == "__main__":
    intents = Intents.default()
    intents.guilds = True
    intents.messages = True
    discord_client = commands.Bot(command_prefix="!", intents=intents)
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    def run_discord_bot():
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(discord_client.start(DISCORD_BOT_TOKEN))
        loop.close()

    discord_bot_thread = threading.Thread(target=run_discord_bot)
    discord_bot_thread.start()

    app.run(debug=True)