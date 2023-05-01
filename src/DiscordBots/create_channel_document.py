import discord
from src.Database.models import Channel

async def create_channel_document(client, channel_id):
    try:
        channel = client.get_channel(channel_id)

        if channel is None:
            raise Exception(f"Channel not found: {channel_id}")

        category = channel.category

        if category is None:
            category_name = "No Category"
        else:
            category_name = category.name

        server_name = channel.guild.name

        # Create a new Channel document with the retrieved information
        new_channel = Channel(
            channel_id=str(channel.id),
            channel_name=channel.name,
            category_name=category_name,
            server_name=server_name
        )

        # Save the new Channel document to the database
        new_channel.save()

        return new_channel

    except discord.Forbidden:
        print(f"Access to channel {channel_id} is forbidden")
        return None

    except Exception as e:
        print(f"An error occurred while fetching channel information: {e}")
        return None
