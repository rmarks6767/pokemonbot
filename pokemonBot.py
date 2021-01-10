
import discord, random
from processors import party_add, party_view
from fight import duel
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

            messageList=message.content.split(" ")
            messageCommand=messageList[1]
            print("Message List 1:",messageCommand)
            if messageCommand == "help" and len(messageCommand)==2:
                await message.channel.send("Commands: \n\t 'party (specified command)'- either 'add (wanted pokemon) or 'list' to view party \n\t 'duel (person)'- challenger a person to a duel \n\t 'fight (target) (move)'- while in a fight, do an attack \n\t 'list (specified list)'- either 'moves', 'parties', or 'pokemon'\n")
                return
            elif messageCommand == "party" and 3 <= len(messageList) <= 4:
                print(messageList)
                #takes in userId and takes in pokemon name if it is party add
                if messageList[2] == "view" and  len(messageList) == 3:
                    response = f'<@!{message.author.id}> ' + party_view(message.author.id)
                    await message.channel.send(response)
                elif messageList[2] == "add" and len(messageList)==4:
                    response = party_add(message.author.id, messageList[3])
                    await message.channel.send(response)
            elif messageCommand == "duel" and len(messageList)==3:
                userId=str(message.author.id)
                opponentId=str(messageList[2]).replace('<@!','').replace('>','')

                response=duel(userId,opponentId)
                await message.channel.send(response)
            elif messageCommand== "fight" and len(messageList)==4:
                await message.channel.send("You are fighting " + str(messageList[2])+ " and used "+ str(messageList[3]))
            elif messageCommand == "list" and len(messageList)==3:
                if messageList[2] == "moves":
                    await message.channel.send("Your moveset")
                elif messageList[2] == "parties":
                    await message.channel.send("Available parties")
                elif messageList[2]== "pokemon":
                    await message.channel.send("Pokemon list")

            else:
                await message.channel.send("INCORRECT COMMAND \n Commands: \n\t 'party (specified command)'- either 'add (wanted pokemon) or 'list' to view party \n\t 'duel (person)'- challenger a person to a duel \n\t 'fight (target) (move)'- while in a fight, do an attack \n\t 'list (specified list)'- either 'moves', 'parties', or 'pokemon'\n")
                return
            # response = get_pokemon()
            # await message.channel.send(response)
        else:
            return
