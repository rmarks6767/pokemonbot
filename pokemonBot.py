
import discord, random
from api import get_pokemon
from processors import party_add
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
            m = message.content.split(' ')
            response = party_add(message.author.id, m[1])
            await message.channel.send(response)
        else:
            return
