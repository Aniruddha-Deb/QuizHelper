import re
import time

import discord
import os
from discord.utils import find, get
from discord.ext import commands
from discord.ext.commands import Bot, ArgumentParsingError
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix="q", intents=intents)

ROLE_QM = "Quizmaster"

TEAM_TEXTS = "Team Text Channels"
TEAM_VCS = "Team Voice Channels"

TEAM_PREFIX = "Team "

class Team:
	
	def __init__(self, team_name, role):
		self.score = 0
		self.name = team_name
		self.role = role
		self.members = []
		self.pounce = ""
		self.text_channel = None
		self.voice_channel = None
	
	def __str__(self):
		return f"{self.name} @ {self.score}: {self.members}"

class TeamCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.qms = []
		self.teams = {}
		self.rt = -1;

	@commands.command(name="tc", help="Load teams into memory")
	@commands.has_any_role(ROLE_QM)
	async def team_load(self, ctx, n: int):
		print("Loading teams")
		guild = ctx.guild
		team_range = range(1,n+1)
		roles = [role for role in guild.roles if role.name.startswith(TEAM_PREFIX) and
				int(role.name.split(" ")[1]) in team_range]
		
		print(roles)
		print(self.rt)
		if self.rt == -1:
			# have not created any teams. Need to create teams
			print("Creating teams")
			for role in roles:
				team = Team(role.name, role)
				tno = int(role.name.split(" ")[1])
				self.teams[role.name] = team
				team.text_channel = get(guild.text_channels, name=f"team-{tno}")
				team.voice_channel = get(guild.voice_channels, name=f"team-{tno}")

		self.rt = time.time()
		members = await guild.fetch_members().flatten()

		for team in self.teams:
			self.teams[team].members.clear()

		for member in members:
			for role in member.roles:
				if role in roles:
					self.teams[role.name].members.append(member)
					break

		for team in self.teams:
			print(self.teams[team])

class PounceCog(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.teams = self.bot.get_cog("TeamCog").teams

	@commands.command(name="p", help="pounce on active question")
	async def pounce(self, ctx, *, arg):
		for role in ctx.author.roles:
			if role.name.startswith(TEAM_PREFIX):
				self.teams[role.name].pounce = arg
				await ctx.send("Your pounce has been registered")

	@commands.command(name="pc", help="Closes pounce")
	@commands.has_any_role(ROLE_QM)
	async def pounce_close(self, ctx):
		pounces = ""
		for team in self.teams:
			pounces += f"{self.teams[team].name}: {self.teams[team].pounce}\n"
			await self.teams[team].text_channel.send("Pounce is now closed")
		
		await ctx.send("Closed pounce")
		await ctx.send(pounces)
	
	@commands.command(name="po", help="Opens pounce")
	@commands.has_any_role(ROLE_QM)
	async def pounce_open(self, ctx):
		for team in self.teams:
			await self.teams[team].text_channel.send("Pounce is now open!")
			self.teams[team].pounce = ""

@bot.event
async def on_ready():
	print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send("You do not have permission to use that command")
	elif isinstance(error, ArgumentParsingError):
		await ctx.send("Syntax error. Did you type that command properly?")
	else: 
		print(error)

bot.add_cog(TeamCog(bot))
bot.add_cog(PounceCog(bot))
bot.run(TOKEN)
	
