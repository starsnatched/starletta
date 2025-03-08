from utils.letta import LettaClient, MessageCreate
from discord.ext import commands
from discord import app_commands
import discord

# from utils.database import *

class Chat(commands.GroupCog, name="ai"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.letta = LettaClient()
        
    @app_commands.command(name="create", description="Create a new AI agent.")
    async def create(self, i: discord.Interaction, name: str):
        await i.response.defer()
        
        agent_list = await self.letta.list_agents(i.user.id)
        if len(agent_list) >= 1:
            await i.followup.send("You have reached the maximum number of agents. Please delete an agent to create a new one.")
            return
        
        agent = await self.letta.create_agent(name, i.user.id)
        # store_agent_id(i.user.id, agent.id)
        
        await i.followup.send(f"Created agent: `{agent.id}`")
        
    @app_commands.command(name="delete", description="Delete an AI agent.")
    async def delete(self, i: discord.Interaction):
        await i.response.defer()
        agent_list = await self.letta.list_agents(i.user.id)
        if len(agent_list) == 0:
            await i.followup.send("You do not have an agent.")
            return
        agent_id = agent_list[0].id
        await self.letta.delete_agent(agent_id)
        await i.followup.send(f"Deleted agent: `{agent_id}`")
        
    @app_commands.command(name="list", description="List all AI agents.")
    async def list(self, i: discord.Interaction):
        await i.response.defer()
        agents = await self.letta.list_agents(i.user.id)
        await i.followup.send("```\n" + "\n".join([f"{agent.id}: {agent.name}" for agent in agents]) + "\n```")
        
    @app_commands.command(name="chat", description="Send a message to an AI agent.")
    async def chat(self, i: discord.Interaction, message: str):
        await i.response.defer()
        # agent_id = get_agent_id(i.user.id)
        agent_list = await self.letta.list_agents(i.user.id)
        agent_id = agent_list[0].id if len(agent_list) >= 1 else None
        if not agent_id:
            await i.followup.send("You do not have an agent. Create one using `/ai create`.")
            return
        # message_list = await self.letta.list_messages(agent_id)
        # message_list.append(MessageCreate(role="user", content=message))
        output = await self.letta.send_message(agent_id, [MessageCreate(role="user", content=message)])
        await i.followup.send("> -# " + "\n> -# ".join(output.messages[0].reasoning.split("\n")) + "\n" + output.messages[1].content)
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        # agent_id = get_agent_id(message.author.id)
        agent_list = await self.letta.list_agents(message.author.id)
        agent_id = agent_list[0].id if len(agent_list) >= 1 else None
        if not agent_id:
            return
        # message_list = await self.letta.list_messages(agent_id)
        # message_list.append(MessageCreate(role="user", content=message.content))
        output = await self.letta.send_message(agent_id, [MessageCreate(role="user", content=message.content)])
        await message.channel.send("> -# " + "\n> -# ".join(output.messages[0].reasoning.split("\n")) + "\n" + output.messages[1].content)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))