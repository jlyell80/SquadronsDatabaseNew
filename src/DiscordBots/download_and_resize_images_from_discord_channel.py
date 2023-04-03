import os
import discord
import aiohttp
from PIL import Image


async def download_image(url: str, images_path: str = "", save_name: str = ""):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(os.path.join(images_path, save_name), "wb") as f:
                    f.write(await resp.read())
    await session.close()


async def download_and_resize_images_from_discord_channel(token: str, channel_id: int, folder_path: str, size: tuple):
    # Create a Discord client object and use the bot token to log in
    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot logged in as {bot.user.name}")
        channel = bot.get_channel(channel_id)

        messages = [msg async for msg in channel.history(limit=1000)]

        print(f"Retrieved {len(messages)} messages from channel {channel.name}")
        attachments = [attachment for message in messages for attachment in message.attachments
                       if attachment.url.endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp'))]

        print(f"Downloading {len(attachments)} attachments...")

        counter = 1
        for i, attachment in enumerate(attachments):
            # Check if the attachment has already been downloaded
            filename = f"{attachment.id}.png"
            filepath = os.path.join(folder_path, filename)
            if os.path.exists(filepath):
                print(f"Skipping {attachment.filename} - already downloaded")
                continue

            # Download the attachment
            print(f"Downloading attachment {counter}/{len(attachments)} - {attachment.filename}...")
            await download_image(attachment.url, images_path=folder_path, save_name=f"{attachment.id}.png")

            # Resize the image
            with Image.open(filepath) as image:
                aspect_ratio = image.size[0] / image.size[1]
                new_height = int(size[0] / aspect_ratio)
                resized_image = image.resize((size[0], new_height))
                resized_image.save(filepath, format="PNG")

            print(f"Downloaded and resized attachment {counter}/{len(attachments)} - {attachment.filename} (ID: {attachment.id}) to {filepath}")

            counter += 1

        await bot.close()

    print("Starting bot...")
    await bot.start(token)