import json
from typing import Optional
from aiohttp import ClientError
import discord
import boto3
import io
import random
import requests
from discord.ext import commands
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_secret(secret_name, region_name) -> Optional[dict]:
    """
    Retrieves a secret from AWS Secrets Manager
    :param secret_name: The name of the secret
    :param region_name: The AWS region where the secret is stored
    :return: The secret as a dictionary
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as error:
        print(f"Error retrieving secret: {error}")
        return None

    return json.loads(response["SecretString"])


 # Discord bot setup
intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="?", intents=intents)

# Google Drive API setup
SERVICE_ACCOUNT_JSON = get_secret("GOOGLE_SERVICE_ACCOUNT_JSON", "eu-west-1")
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_JSON, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=creds)


# Function to search for the image in the specified Google Drive folder
async def search_image(image_name, folder_id):
    try:
        image_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
        query = " or ".join(
            [
                f"(name = '{image_name}.{ext}' and mimeType = 'image/{ext if ext != 'jpg' else 'jpeg'}')"
                for ext in image_extensions
            ]
        )
        query = f"({query}) and trashed = false and '{folder_id}' in parents"
        response = (
            drive_service.files().list(q=query, fields="nextPageToken, files(id, name, webContentLink)").execute()
        )
        items = response.get("files", [])

        if not items:
            return None

        return items[0]
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


# Discord bot command
@bot.command(name="img", help="Searches for specified image in Google Drive and sends it to the channel")
async def img(ctx, image_name: str):
    image = await search_image(image_name, DRIVE_FOLDER_ID)

    if image:
        # Download the image
        response = requests.get(image["webContentLink"])
        image_data = io.BytesIO(response.content)

        # Send the image as an attachment
        file = discord.File(image_data, filename=f"{image_name}.jpg")
        await ctx.send(file=file)
    else:
        await ctx.send("Sorry, I couldn't find that image.")


@bot.command(name="chocolatine", help="Randomly chooses a member to bring breakfast")
async def chocolatine(ctx):
    # Get all members with the 'Breakfast' role
    breakfast_role = discord.utils.get(ctx.guild.roles, name="Breakfast")
    breakfast_members = [member for member in ctx.guild.members if breakfast_role in member.roles]

    # Randomly choose a member and send a message with their mention
    if breakfast_members:
        chosen_member = random.choice(breakfast_members)
        await ctx.send(
            f"This week, {chosen_member.mention} will bring us a nice breakfast!\n_PLEASE screenshot this message_"
        )
    else:
        await ctx.send("No members with the 'Breakfast' role were found.")


@bot.command(name="oliviades", help="Posts a random oliviade message from the specific channel")
async def oliviades(ctx):
    channel = bot.get_channel(OLIVIADES_CHANNEL_ID)
    await post_random_citation(ctx, channel)


# Helper function to post a random citation message
async def post_random_citation(ctx, channel):
    citation_messages = []
    async for message in channel.history(limit=1000):
        if message.content.startswith('"'):
            citation_messages.append(message.content)
    if citation_messages:
        await ctx.send(random.choice(citation_messages))
    else:
        await ctx.send("Sorry, I couldn't find any citation messages.")


def start_bot(discord_bot_token: str):
    if discord_bot_token:
        bot.run(discord_bot_token)
    else:
        print("Error: Unable to retrieve Discord bot token from Secrets Manager.")


if __name__ == "__main__":
    bot_secrets = get_secret("giorno_bot_secrets", "eu-west-1")
    if bot_secrets:
        DRIVE_FOLDER_ID = bot_secrets["drive_folder"]
        OLIVIADES_CHANNEL_ID = int(bot_secrets["oliviades_channel"])
        start_bot(bot_secrets["token"])
    else:
        print("Error: Unable to retrieve the bot's secrets from Secrets Manager.")
