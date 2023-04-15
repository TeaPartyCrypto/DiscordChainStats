from dotenv import load_dotenv
from os import getenv
load_dotenv()
bot_token = getenv("MARKET_CAP_TOKEN")

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_market_cap

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


if __name__ == "__main__":
    client.run(bot_token)
