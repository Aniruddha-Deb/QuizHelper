import discord
import messenger
import os
from discord.ext import commands
from discord.ext.commands import Bot
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
	async def team_create(self, ctx, args):
		print("create team: ", args)

	@commands.command(name="ta", help="Add members to given team")
	@commands.has_any_role(ROLE_QM)
	async def team_add(self, ctx, args):
		print("add to team: ", args)

	@commands.command(name="tr", help="Remove members from given team")
	@commands.has_any_role(ROLE_QM)
	async def team_remove(self, ctx, args):
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

bot.add_cog(TeamCog(bot))
bot.add_cog(PounceCog(bot))
bot.run(TOKEN)
	
