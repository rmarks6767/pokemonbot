from file_operations import save_file, read_file
from api import find_pokemon, find_move_flavor_text
import ast

def find_move_names(moves):
  names = []

  for move in moves:
    names.append(move['name'])

  return names

################# Party commands

def party_parser(party):
  new_party = {}
  party_vals= party.split('[:]')

  new_party['userId'] = party_vals[0]
  new_party['pokemonName'] = party_vals[1]
  new_party['pokemon'] = ast.literal_eval(party_vals[2])

  return new_party

# @PokemonBot party add [pokemon]
def party_add(userId, pokemonName):
  pokemon = find_pokemon(pokemonName.lower())

  if pokemon != None:
    parties = read_file('parties.txt')

    for party in parties:
      split_party = party.split('[:]')
      if (split_party[0] == str(userId)):
        return f'<@!{userId}> You already have a party, you must abandon it to create a new one!'

    parties.append(f'{userId}[:]{pokemonName}[:]{pokemon}\n')

    save_file('parties.txt', parties)

    return f'Adding {pokemonName} to your party! Your move set will be {find_move_names(pokemon["moves"])}'
  else:
    return 'Could not find that pokemon, also note that only gen 1 is allowed'

# @PokemonBot party abandon
def party_abandon(userId):
  parties = read_file('parties.txt')

  file = []

  for party in parties:
    split_party = party.split('[:]')

    if split_party[0] != str(userId):
      file.append(party)
  
  save_file('parties.txt', file)

  return f'<@!{userId}> Successfully abandoned your party'

# @PokemonBot party replace [pokemon]
def party_replace(userId, pokemonName):
  party_abandon(userId)
  return party_add(userId, pokemonName)

# @PokemonBot party view
def party_view(userId): 
  parties = read_file('parties.txt')

  for p in parties:
    party = party_parser(p)

    if (party['userId'] == str(userId)):
      return f'Your current party is {party["pokemonName"]} with the moveset {find_move_names(party["pokemon"]["moves"])}'

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

def help_move(userId, moveText):
  parties = read_file('parties.txt')

  move = find_move_flavor_text(moveText)
  
  if not move:
    return 'That is not a valid move'
  else:
    return move