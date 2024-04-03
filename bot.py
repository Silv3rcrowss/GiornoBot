from typing import Any
import discord
import io
import random
import requests
from discord.ext import commands
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common import get_secret
from personal_assitant import Conversation


class GiornoBot(commands.Bot):
    conversation: dict[str, Conversation]
    drive_service: Any
    oliviade_channel_id: str
    drive_id_folder: str
    bot_token: str

    def __init__(self, command_prefix: str):
        intents = discord.Intents.all()
        intents.members = True
        intents.messages = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        self._initialize_bot_secrets()
        self._initialize_google_service_account()
        self.conversation = {}
        self.add_commands()
        self.run(token=self.bot_token)

    async def search_image(self, image_name, folder_id):
        """
        Searches for the specified image in the specified Google Drive folder.
        :param image_name: The name of the image to search for
        :param folder_id: The ID of the Google Drive folder to search in
        :return: The Google Drive file object of the found image, or None if not found
        """
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
                self.drive_service.files()
                .list(q=query, fields="nextPageToken, files(id, name, webContentLink)")
                .execute()
            )
            items = response.get("files", [])

            if not items:
                return None

            return items[0]
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def add_commands(self):
        @self.command(name="giorno", help="Replies with text generation")
        async def giorno(ctx, *args):
            """
            Replies with AI text generation
            :param ctx: The context of the command
            :param prompt: The prompt to generate text from
            :return: None
            """
            author = ctx.author
            prompt = f'{author.name}: {" ".join(args)}'
            print(f"Author: {author.name}")
            print(f"Received prompt: {prompt}")
            prompt_history = ""
            skip_prompt = True
            async for message in ctx.channel.history(limit=10):
                if skip_prompt:
                    skip_prompt = False
                    continue
                if message.author == self.user:
                    break
                prompt_history = (
                    f"{message.author}: {message.content}\n{prompt_history}"
                )
            prompt = f"*Message history*\n{prompt_history}\n*Prompt*\n{prompt}"
            print(prompt)
            if ctx.channel.id not in self.conversation.keys():
                self.conversation[ctx.channel.id] = Conversation()
            response = self.conversation[ctx.channel.id].run_and_retrieve_message(
                prompt=prompt
            )
            await ctx.send(response)

        @self.command(name="reset", help="Resets the conversation")
        async def reset_conversation(self, ctx):
            self.conversation.reset_run()
            await ctx.send("Conversation reset.")

        @self.command(
            name="img",
            help="Searches for specified image in Google Drive and sends it to the channel",
        )
        async def img(ctx, image_name: str):
            """
            Searches for the specified image in the specified Google Drive folder and sends it to the channel.
            :param ctx: The context of the command
            :param image_name: The name of the image to search for
            :return: None
            """
            image = await self.search_image(image_name, self.drive_id_folder)

            if image:
                # Download the image
                response = requests.get(image["webContentLink"])
                image_data = io.BytesIO(response.content)

                # Send the image as an attachment
                file = discord.File(image_data, filename=f"{image_name}.jpg")
                await ctx.send(file=file)
            else:
                await ctx.send("Sorry, I couldn't find that image.")

        @self.command(
            name="chocolatine", help="Randomly chooses a member to bring breakfast"
        )
        async def chocolatine(ctx):
            breakfast_role = discord.utils.get(ctx.guild.roles, name="Breakfast")
            breakfast_members = [
                member for member in ctx.guild.members if breakfast_role in member.roles
            ]

            if breakfast_members:
                chosen_member = random.choice(breakfast_members)
                await ctx.send(
                    f"This week, {chosen_member.mention} will bring us a nice breakfast!\n_PLEASE screenshot this message_"
                )
            else:
                await ctx.send("No members with the 'Breakfast' role were found.")

        @self.command(
            name="oliviade",
            help="Posts a random oliviade message from the specific channel",
        )
        async def oliviades(ctx):
            channel = bot.get_channel(self.oliviade_channel_id)
            citation_messages = []
            async for message in channel.history(limit=1000):
                if message.content.startswith('"'):
                    citation_messages.append(message.content)
            if citation_messages:
                await ctx.send(random.choice(citation_messages))
            else:
                await ctx.send("Sorry, I couldn't find any citation messages.")

    def _initialize_bot_secrets(self):
        bot_secrets = get_secret(
            secret_name="giorno_bot_secrets", region_name="eu-west-1"
        )
        if bot_secrets:
            self.drive_id_folder = bot_secrets["drive_folder"]
            self.oliviade_channel_id = int(bot_secrets["oliviades_channel"])
            self.bot_token = bot_secrets["token"]
        else:
            raise Exception(
                "Error: Unable to retrieve the bot's secrets from Secrets Manager."
            )

    def _initialize_google_service_account(self):
        service_account_json = get_secret(
            secret_name="GOOGLE_SERVICE_ACCOUNT_JSON", region_name="eu-west-1"
        )
        scopes = ["https://www.googleapis.com/auth/drive.readonly"]
        creds = service_account.Credentials.from_service_account_info(
            info=service_account_json, scopes=scopes
        )
        self.drive_service = build("drive", "v3", credentials=creds)


if __name__ == "__main__":
    bot = GiornoBot(command_prefix="?")
