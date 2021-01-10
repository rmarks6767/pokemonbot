
import discord, random
from processors import party_add, party_view, party_abandon, party_replace, help_move
from fight import duel
from fight import executeMove


class PokemonBot(discord.Client):
    async def on_ready(self):
        print(f'(self.user) has connected to Discord!')
    async def on_message(self,message):
        print(message.content)
        if message.author == self.user:
            return

        if str(self.user.id) in str(message.content):
            messageList=message.content.split(" ")
            messageCommand=messageList[1]

            if messageCommand == "help":
                if len(messageList)==2:
                    await message.channel.send("Commands: \n\tparty [view | abandon] --- View or abandon your current party \n\tparty [add | replace ] [pokemon] --- Add or replace your current party with a new pokemon \n\tduel [@person] [level = 5] --- challenge a person to a duel at a given level (if none is provided will be 5) \n\texecute-move [@target] [move] --- Execute a move in an active duel on a given player \n\tlist [moves | parties] --- List your current party move set or available duelable parties\n")
                if len(messageList)==3:
                    response = help_move(message.author.id, messageList[2])
                    await message.channel.send(response)
            elif messageCommand == "party":
                if messageList[2] == "view" and  len(messageList) == 3:
                    response = f'<@!{message.author.id}> ' + party_view(message.author.id)
                    await message.channel.send(response)
                elif messageList[2] == "add" and len(messageList) == 4:
                    response = party_add(message.author.id, messageList[3])
                    await message.channel.send(response)
                elif messageList[2] == "abandon" and len(messageList) == 3:
                    response = party_abandon(message.author.id)
                    await message.channel.send(response)
                elif messageList[2] == "replace" and len(messageList) == 4:
                    response = party_replace(message.author.id, messageList[3])
                    await message.channel.send(response)
            elif messageCommand == "duel":
                userId=str(message.author.id)
                opponentId=str(messageList[2]).replace('<@!','').replace('>','')
                level = 5
                if len(messageList) == 4:
                    level = int(messageList[3])

                response=duel(userId,opponentId, level)
                await message.channel.send(response)
            elif messageCommand== "execute-move" and len(messageList)==4:
                userId=str(message.author.id)
                opponentId=str(messageList[2]).replace('<@!','').replace('>','')
                response=executeMove(messageList[3],opponentId,userId)
                await message.channel.send(response)
            elif messageCommand == "list" and len(messageList)==3:
                if messageList[2] == "moves":
                    await message.channel.send("Your moveset")
                elif messageList[2] == "parties":
                    await message.channel.send("Available parties")
                elif messageList[2]== "pokemon":
                    await message.channel.send("Pokemon list")
            else:
                await message.channel.send("Commands: \n\tparty [view | abandon] --- View or abandon your current party \n\tparty [add | replace ] [pokemon] --- Add or replace your current party with a new pokemon \n\tduel [@person] [level = 5] --- challenge a person to a duel at a given level (if none is provided will be 5) \n\texecute-move [@target] [move] --- Execute a move in an active duel on a given player \n\tlist [moves | parties] --- List your current party move set or available duelable parties\n")
        return

#if message.author.name == "River":
#    await message.channel.send("Shut up clown 🤡")
#print(message.content)
#print(self.user.id)