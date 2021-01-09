
import discord, random
from api import get_pokemon
class PokemonBot(discord.Client):

    async def on_ready(self):
        print(f'(self.user) has connected to Discord!')
    async def on_message(self,message):
        print(message.content)
        if message.author == self.user:
                return
        #if message.author.name == "River":
        #    await message.channel.send("Shut up clown 🤡")

        #print(message.content)
        #print(self.user.id)
        if str(self.user.id) in str(message.content):
            response= get_pokemon()
            await message.channel.send(response)
        else:
            return
