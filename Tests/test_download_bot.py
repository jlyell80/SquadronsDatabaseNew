import asyncio
import os

from src.DiscordBots.download_and_resize_images_from_discord_channel import \
    download_and_resize_images_from_discord_channel


async def main():
    token = os.getenv('DISCORD_BOT_TOKEN')

    channel_id = 1015967860918591530  # Replace with the ID of your Discord channel
    download_folder = './downloads/'  # Replace with the folder path where you want to save the downloaded images
    size = (720, 720)  # Replace with the desired size of the images

    try:
        await download_and_resize_images_from_discord_channel(token, channel_id, download_folder, size)
    except ValueError as e:
        print(f'Error: {e}')


asyncio.run(main())
