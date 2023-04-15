import dotenv
dotenv.load_dotenv()

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_current_supply, node_connection

from os import getenv


bot_token = getenv("CIRCULATING_SUPPLY_TOKEN")
intents = Intents.default()
client = Client(intents=intents)


@tasks.loop(minutes=5)
async def update_supply():
    current_supply = get_current_supply(node_connection())
    await client.change_presence(
        activity=Activity(
            type=ActivityType.watching,
            name=f"{round(current_supply, 1)}"
        )
    )


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    update_supply.start()


client.run(bot_token)
