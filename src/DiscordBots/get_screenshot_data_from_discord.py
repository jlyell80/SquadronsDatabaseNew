import discord
import aiohttp
import io
from PIL import Image
from src.Database.models import Screenshot
import asyncio


async def download_image_data(session, url, timeout=30):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
        async with session.get(url) as response:
            return await response.read()

async def resize_image(image_data, target_height):
    with io.BytesIO(image_data) as input_buffer, io.BytesIO() as output_buffer:
        image = Image.open(input_buffer)
        aspect_ratio = float(image.width) / float(image.height)
        target_width = int(target_height * aspect_ratio)

        image = image.resize((target_width, target_height))
        image.save(output_buffer, format='PNG')
        resized_image_data = output_buffer.getvalue()

    return resized_image_data


async def process_message(session, message, target_height):
    if not message.author.bot and message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Check if the image has already been uploaded using the image ID
                existing_screenshot = Screenshot.objects(image_id=attachment.id).first()
                if existing_screenshot:
                    continue

                image_data = await asyncio.wait_for(download_image_data(session, attachment.url), timeout=30)  # Adjust the timeout value as needed
                resized_image_data = await resize_image(image_data, target_height)

                # Create a new document for each attachment and save it to the database
                screenshot_document = Screenshot(
                    message_id=str(message.id),
                    message_data={
                        "author": str(message.author),
                        "timestamp": message.created_at,
                        "content": message.content,
                        "channel_id": str(message.channel.id),
                        "channel_name": message.channel.name
                    },
                    image_id=attachment.id,
                    image_url=attachment.url,
                    image_data=resized_image_data,
                    game_id=None  # You can update this field when you have the game_id
                )
                screenshot_document.save()
                print(f"Added new message with ID {message.id} and attachment ID {attachment.id}")

    return bool(message.attachments)  # Return True if there were any attachments in the message




class ScreenshotCollector(discord.Client):
    def __init__(self, channel_id, target_height, *args, **kwargs):
        self.channel_id = channel_id
        self.target_height = target_height
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        super().__init__(*args, intents=intents, **kwargs)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        target_channel = self.get_channel(int(self.channel_id))
        image_count = 0

        async for message in target_channel.history(limit=1000):  # Adjust the limit as needed
            image_processed = await process_message(self.session, message, self.target_height)
            if image_processed:
                image_count += 1

        print(f"Processed {image_count} images from channel {self.channel_id}")

    async def close(self):
        await self.session.close()
        await super().close()