from file_operations import save_file, read_file
from api import find_pokemon, get_pokemon
import ast

def party_parser(party):
  new_party = {}
  party_vals= party.split(':')

  print(party_vals)

  new_party['userId'] = party_vals[0]
  new_party['pokemonName'] = party_vals[1]
  new_party['pokemonId'] = party_vals[2]
  new_party['moves'] = ast.literal_eval(party_vals[3])

  return new_party

# Party commands
# @PokemonBot party add [pokemon]
def party_add(userId, pokemon):
  pokemon_id = find_pokemon(pokemon.lower())
  moves = get_pokemon(pokemon_id)

  if pokemon_id != None and str(pokemon_id) <= '151':
    parties = read_file('parties.txt')

    parties.append(f'{userId}:{pokemon}:{pokemon_id}:{str(moves)}\n')

    save_file('parties.txt', parties)

    return f'Adding {pokemon} to your party! Your move set will be {moves}'
  else:
    return 'Could not find that pokemon, also note that only gen 1 is allowed'

# @PokemonBot party view
def party_view(userId): 
  parties = read_file('parties.txt')

  for p in parties:
    party = party_parser(p)

    if (party['userId'] == str(userId)):
      return f'Your current party is {party["pokemonName"]} with the moveset {party["moves"]}'

  return 'Your party is empty!'


def fight(userId, fightingId, move):
  parties = read_file('parties.txt')

  userParty = None
  fightingParty = None

  for p in parties:
    party = party_parser(p)

    if party['userId'] == str(userId):
      userParty = party
    if party['userId'] == str(fightingId):
      fightingParty = party

  