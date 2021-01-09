import os, discord
from dotenv import load_dotenv
from pokemonBot import PokemonBot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client= PokemonBot()
client.run(TOKEN)