import re

import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot, ArgumentParsingError
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = Bot(command_prefix="q")

ROLE_P = "Participant"
ROLE_QM = "Quizmaster"
TEAMS = "Teams"

class TeamCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.participants = { ROLE_QM:[], TEAMS:{} }

	@commands.command(name="tc", help="Create a team with the following members")
	@commands.has_any_role(ROLE_QM)
	async def team_create(self, ctx, team, *members: discord.User):
		# ? check first if the given team exists
		# then check if any of the participants is already in a team
		# if both of above are good, create the team and stuff
		print("create team: ", team, members)
		if len(members) < 1:
			print("Syntax error")
			raise ArgumentParsingError()

		if team in self.participants[TEAMS].keys():
			print("Team exists")
			await ctx.send("That Team already exists! Aborting command")
		else:
			# create team
			print("Creating team")
			self.participants[TEAMS][team] = members
			guild = ctx.guild
			role = next((r for r in guild.roles if r.name == team), None)
			if role == None:
				# create role
				print("Creating role")
				role = await guild.create_role(name=team)
			
			for member in members:
				print("Adding member to role")
				await member.add_roles(role)
			
			# create chatroom + VC for team members
			qm_role = discord.utils.get(guild.roles, name=ROLE_QM)
			overwrites = {
				guild.default_role: discord.PermissionOverwrite(read_messages=False),
				guild.me: discord.PermissionOverwrite(read_messages=True),
				role: discord.PermissionOverwrite(read_messages=True),
				qm_role: discord.PermissionOverwrite(read_messages=True)
			}
			await guild.create_text_channel(team, overwrites=overwrites)
			await guild.create_voice_channel(team, overwrites=overwrites)

			await ctx.send("Successfully created team")

	@commands.command(name="ta", help="Add members to given team")
	@commands.has_any_role(ROLE_QM)
	async def team_add(self, ctx, *args):
		guild = ctx.guild
		await guild.create_role("Team1")

	@commands.command(name="tr", help="Remove members from given team")
	@commands.has_any_role(ROLE_QM)
	async def team_remove(self, ctx, *args):
		print("remove from team: ", args)

class PounceCog(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="p", help="pounce on active question")
	@commands.has_any_role(ROLE_P, ROLE_QM)
	async def pounce(self, ctx, *, arg):
		print(arg)
		await ctx.send("Your pounce has been registered")


@bot.event
async def on_ready():
	print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send("You do not have permission to use that command")
	elif isinstance(error, ArgumentParsingError):
		await ctx.send("Syntax error. Did you type that command properly?")

bot.add_cog(TeamCog(bot))
bot.add_cog(PounceCog(bot))
bot.run(TOKEN)
	
