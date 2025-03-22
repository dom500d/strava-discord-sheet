# This example requires the 'message_content' intent.
import os
import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()

import discord
import dotenv
import ssl
import certifi
import aiohttp

from functools import partial, wraps
import discord
from discord.ext import commands
from cache import FileCache
import logging

logging.basicConfig(filename="botlog.txt")

class Bot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix="/", intents=intents)
        self.bot.event(self.on_ready)
        self.add_command("command1", Bot.some_command)
        self.add_command("add_segment", Bot.add_segment)
        self.add_command("list_segments", Bot.list_segments)
        self.add_command("remove_segment", Bot.remove_segment)
        self.add_command("list_users", Bot.list_users)
        self.add_command("add_user", Bot.add_user)
        self.cache = FileCache()
        # self.add_command("help", "List all commands and their descriptions", Bot.help_command)

    def add_command(self, name, f):
        self.bot.command(name=name)(wraps(f)(partial(f, self)))

    def run(self, token):
        try:
            self.bot.run(token)
        except KeyboardInterrupt:
            logging.info("Bot stopped via Ctrl+C. Performing cleanup.")
            # You can call your cleanup function here if needed
            self.on_shutdown()
        finally:
            logging.info('Bot has been shut down.')
        

    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")
        for guild in self.bot.guilds:
            print(guild)
        print(f"Loading file cache from {self.cache.cache_file}")

    def on_shutdown(self):
        print("SESES)")
        self.cache._save_cache()

    async def some_command(self, ctx, arg1: str = commands.parameter(default="Here be default", description="Here be description")):
        await ctx.send("Hello world!")

    async def add_segment(self, ctx, segment_name: str = commands.parameter(default="Torrey Pines", description="Add this segment to be watched! You need to enclose the segment in quotation marks.")):
        current_segment_list = self.cache.get("segments", [])
        if segment_name  in current_segment_list:
            await ctx.send(f"{segment_name} is already being tracked!")
            return
        
        current_segment_list.append(segment_name)
        self.cache.set("segments", current_segment_list)
        await ctx.send(segment_name)

    async def list_segments(self, ctx):
        current_segment_list = self.cache.get("segments", [])
        await ctx.send("**Segments currently being tracked:**")
        send_string = ""
        for index, segment in enumerate(current_segment_list):
            send_string += f"{index}. {segment} \n"

        await ctx.send(send_string)
    
    async def remove_segment(self, ctx, segment_name: str = commands.parameter(default=None, description="Add this segment to be watched! You need to enclose the segment in quotation marks.")):
        current_segment_list = self.cache.get("segments", [])
        if segment_name is not None:
            if segment_name in current_segment_list:
                current_segment_list.remove(segment_name)
                self.cache.set("segments", current_segment_list)
                await ctx.send(f"{segment_name} has been removed from the list!")
            else:
                await ctx.send(f"{segment_name} is not in the list, please double check if you spelled the segment correctly!")
        else:
            await ctx.send("You need to specify the segment name, try /list_segments")

    async def add_user(self, ctx, user_name: str = commands.parameter(default=None, description="Add a strava user to track segment bests!")):
        current_user_list = self.cache.get("users", [])
        if user_name is not None:
            if user_name in current_user_list:
                await ctx.send(f"{user_name} is already added to the list")
                return
            else:
                current_user_list.append(user_name)
                self.cache.set("users", current_user_list)
                await ctx.send(f"{user_name} has been added to the list")
                return
        else:
            await ctx.send("You need to specify the user name")

    async def list_users(self, ctx):
        current_user_list = self.cache.get("users", [])
        await ctx.send("**Users currently being tracked:**")
        send_string = ""
        for index, segment in enumerate(current_user_list):
            send_string += f"{index}. {segment} \n"

        await ctx.send(send_string)

config = dotenv.dotenv_values(".env")

# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

# client.run(config['BOT_TOKEN'])

if __name__ == '__main__':
    le_bot = Bot()
    le_bot.run(config['BOT_TOKEN'])


