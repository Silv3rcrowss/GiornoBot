import discord
import random
from discord.ext import commands
from datetime import datetime


TOKEN = "OTIyOTY3ODczODg5MTIwMjY4.YcJK0Q.3De7nzpXDgbONAIDZ3-X8Sj1MEQ"
client = discord.Client()
bot = commands.Bot(command_prefix="!")


@bot.command()
async def play(ctx):
    pass



@bot.command(aliases=["sunland", "bg", "alexandre"])
async def sunny(ctx):
    sunny_chat = []
    channel = bot.get_channel(794361017479856148)
    async for message in channel.history(limit=500):
        user_message = str(message.content)
        if user_message.startswith('"'):
            quote = user_message.split('"')[1]
            author = "Sunland"
            quote_date = message.created_at.strftime("%d/%m/%Y")
            if not user_message.endswith('"'):
                author = user_message.split('"')[-1].replace("-", " ").strip()
            sunny_chat.append(f'"{quote}"\n-{author} ({quote_date})')
    await ctx.send(random.choice(sunny_chat))


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.command(
    aliases=["vathana", "vathanal", "vijay", "yasuo-main", "lol", "vathanalakshan"]
)
async def vanathal(ctx):
    vatha_chat = []
    channel = bot.get_channel(748241419382292491)
    async for message in channel.history(limit=500):
        user_message = str(message.content)
        if user_message.startswith('"'):
            quote = user_message.split('"')[1]
            author = "Vathana"
            quote_date = message.created_at.strftime("%d/%m/%Y")
            if not user_message.endswith('"'):
                author = user_message.split('"')[-1].replace("-", " ").strip()
            vatha_chat.append(f'"{quote}"\n-{author} ({quote_date})')
    await ctx.send(random.choice(vatha_chat))


@bot.command()
async def dio(ctx):
    await ctx.send(" hō hō ?…mukatte kuru noka ?")
    await ctx.send(" nige zuni kono dio ni chikazuite kuru noka ?")


async def gen(ctx, message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f"{username}: {user_message} ({channel})")
    if message.author == client.user:
        return

    if user_message.lower() == "wisdom":
        list_of_masterclases = client.get_channel(923005189550661653)
        async for masterclass in list_of_masterclases.history(limit=600):
            user_message = str(masterclass.content)
            if user_message.startswith('"'):
                quote = user_message
                author = "Vathana"
                quote_date = masterclass.created_at.strftime("%d/%m/%Y")
                if "-" in user_message:
                    quote = user_message.split("-")[0]
                    if "0" not in user_message.split("-")[1].split(" ")[0]:
                        author = user_message.split("-")[1].split(" ")[0]
            print(f"{quote}\n-{author} {quote_date}")
            await message.channel.send(f"{quote}\n-{author} {quote_date}")
        return

    elif user_message.lower() == "dio!":
        await message.channel.send(" hō hō ?…mukatte kuru noka ?")
        await message.channel.send(" nige zuni kono dio ni chikazuite kuru noka ?")
        return


bot.run(TOKEN)


# Add pictures treatment
