import  requests, random, math

base_URL="https://pokeapi.co/api/v2/"

def calculate_stat(base_stat, level):
    return math.floor((((base_stat + random.randint(16,31)) * 2) * level) / 100) + 5

def calculate_health(base_health, level):
    return math.floor((((base_health + random.randint(16,31)) * 2) * level) / 100) + 5 + level

def build_stat_changes(stat_changes):
    stats = []

    for stat in stat_changes:
        stats.append({
            'change': stat['change'],
            'name': stat['stat']['name']
        })

    return stats

def build_damage_class_relations(damage_class):
    response = requests.get(damage_class['url'])
    data = response.json()

    damage = {}

    relations = data['damage_relations']

    for d in ['double_damage_to', 'half_damage_to', 'no_damage_to']:
        damage[d] = []
        for double in relations[d]:
            damage[d].append(double['name'])

    return damage

def build_types(types):
    built_types = []

    for t in types:
        built_types.append(t['type']['name'])

    return built_types

def find_flavor_text(flavor_texts):
    for flavor in flavor_texts:
        if flavor['language']['name'] == 'en':
            return flavor['flavor_text']

def build_moves(moves):
    chosenMoves = []

    def contains(list, filter):
        for x in list:
            if filter(x):
                return True
        return False

    while len(chosenMoves) < 4 :
        randomIndex = random.randint(0, len(moves) - 1)
        move = moves[randomIndex]['move']
        
        if len(chosenMoves) == len(moves): 
            break

        if not contains(chosenMoves, lambda x: x['name'] == move['name']):

            response = requests.get(move['url'])
            data = response.json()

            chosenMoves.append({
                'name': move['name'],
                'power': data['power'],
                'pp': data['pp'],
                'accuracy': data['accuracy'],
                'flavor_text': find_flavor_text(data['flavor_text_entries']),
                'type': data['type']['name'],
                'damage_class': {
                    'type': data['damage_class']['name'],
                    'relations': build_damage_class_relations(data['type'])
                },
                'stat_changes': build_stat_changes(data['stat_changes'])
            })  
    return chosenMoves

def find_pokemon(name):  
    response = requests.get(f'{base_URL}/pokemon/{name}')
    data = response.json()

    level = 40

    if data != None:
        pokemon={
            'id': data['id'],
            'weight': data['weight'],
            'level': level,
            'types': build_types(data['types']),
            'stats': {
                'hp': calculate_health(data['stats'][0]['base_stat'], level),
                'attack': calculate_stat(data['stats'][1]['base_stat'], level),
                'defense': calculate_stat(data['stats'][2]['base_stat'], level),
                'special-attack': calculate_stat(data['stats'][3]['base_stat'], level),
                'special-defense': calculate_stat(data['stats'][4]['base_stat'], level),
                'speed': calculate_stat(data['stats'][5]['base_stat'], level),
            },
            'moves': build_moves(data['moves'])
        }

        return pokemon
    else:
        return None

def find_move_flavor_text(moveText):
    response = requests.get(f'{base_URL}move/{moveText}')

    if response != None:
        data = response.json() 

        return f'**{data["name"]}**\n{find_flavor_text(data["flavor_text_entries"])}'
    else:
        return None