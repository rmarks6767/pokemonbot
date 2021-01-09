from file_operations import save_file, read_file
from api import find_pokemon, get_pokemon

# Party commands
# @PokemonBot party add [pokemon]
def party_add(userId, pokemon):
  pokemon_id = find_pokemon(pokemon.lower())
  moves = get_pokemon(pokemon_id)

  if (pokemon_id != None):
    parties = read_file('parties.txt')

    parties.append(f'{userId},{pokemon},{pokemon_id},moveset:{str(moves)}')

    save_file('parties.txt', parties)

    return f'Adding {pokemon} to your party! Your move set will be {moves}'
  else:
    return 'Could not find that pokemon, only gen 1 is allowed'

# @PokemonBot party view
def party_view(userId):
  y = 0
