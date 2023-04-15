import dotenv
dotenv.load_dotenv()

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_current_hashrate, format_hashrate

from os import getenv


bot_token = getenv("HASHRATE_TOKEN")
intents = Intents.default()
client = Client(intents=intents)


@tasks.loop(minutes=5)
async def update_hashrate():
    current_hashrate = get_current_hashrate()[0]
    if current_hashrate is None:
        return
    await client.change_presence(
        activity=Activity(
            type=ActivityType.watching,
            name=f"{format_hashrate(float(current_hashrate))}"
        )
    )


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    update_hashrate.start()


client.run(bot_token)
