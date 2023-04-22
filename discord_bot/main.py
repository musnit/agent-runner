import os
import discord
from dotenv import load_dotenv
from discord import app_commands
import requests
import json

load_dotenv()

DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
DISCORD_GUILD_ID = os.environ["DISCORD_GUILD_ID"]

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Open the file for reading
with open("bot_config.json", "r") as file:
    # Load JSON data from the file
    bot_config = json.load(file)


@tree.command(
    name="commit_summary",
    description="Get a summary of the last 2 weeks of Spinamp github commits",
    guild=discord.Object(id=951969750806855740),
)
async def commit_summary(interaction):
    await interaction.response.send_message(
        "Commit Summary: I'm on it! Gimme a minute..."
    )
    url = "http://localhost:8000/run_agent"
    data = {
        "name": "changelog",
        "input": bot_config["changelog_repos"],
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        api_data = response.json()
        content = api_data["result"]["content"]
        await interaction.followup.send(str(content))
    else:
        await interaction.followup.send("An error occured while summarizing the commit")


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=DISCORD_GUILD_ID))
    print("Ready!")


client.run(DISCORD_BOT_TOKEN)
