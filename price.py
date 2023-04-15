from dotenv import load_dotenv
from os import getenv
load_dotenv()
bot_token = getenv("PRICE_TOKEN")

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_current_price

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


if __name__ == "__main__":
    client.run(bot_token)
