from dotenv import load_dotenv
from os import getenv
load_dotenv()
bot_token = getenv("CIRCULATING_SUPPLY_TOKEN")

from discord import Intents, Client, Activity, ActivityType
from discord.ext import tasks
from tools import get_current_supply, node_connection

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


if __name__ == "__main__":
    client.run(bot_token)
