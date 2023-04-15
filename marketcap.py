import dotenv
dotenv.load_dotenv()

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_market_cap
from os import getenv

bot_token = getenv("MARKET_CAP_TOKEN")
intents = Intents.default()
client = Client(intents=intents)


@tasks.loop(minutes=5)
async def update_market_cap():
    current_market_cap = get_market_cap()
    if current_market_cap is None:
        return
    await client.change_presence(
        activity=Activity(
            type=ActivityType.watching,
            name=f"${round(current_market_cap, 2)}"
        )
    )


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    update_market_cap.start()


client.run(bot_token)
