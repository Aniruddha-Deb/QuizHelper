import os
import re
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
	print(f"{client.user} has connected to Discord!")

def is_in_team(user):
	for role in user.roles:
		if role.name.startswith("Team"):
			return True
	return False

def get_team(user):
	for role in user.roles:
		if role.name.startswith("Team"):
			return re.sub(r"(\s*)Team(\s*)", "", role.name)
	return None

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	text = message.content

	if text.startswith('qp') and is_in_team(message.author):
		team = get_team(message.author)
		pounce = re.sub(r"(\s*)qp(\s*)", "", text)
		print( f"Team {team}: {pounce}" )
		await message.channel.send("Your pounce has been registered")

client.run(TOKEN)
