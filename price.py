import dotenv
dotenv.load_dotenv()

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_current_price

from os import getenv


bot_token = getenv("PRICE_TOKEN")
intents = Intents.default()
client = Client(intents=intents)


@tasks.loop(minutes=5)
async def update_price():
    current_price = get_current_price()[0]
    if current_price is None:
        return
    await client.change_presence(
        activity=Activity(
            type=ActivityType.watching,
            name=f"${round(float(current_price), 8)}"
        )
    )


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    update_price.start()


client.run(bot_token)
