import  requests, random

base_URL="https://pokeapi.co/api/v2/pokemon/"

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
    response = requests.get(base_URL + name)
    data = response.json()

    if data != None:
        pokemon={
            'id': data['id'],
            'weight': data['weight'],
            'level': '5',
            'types': build_types(data['types']),
            'stats': {
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
                'special-attack': data['stats'][3]['base_stat'],
                'special-defense': data['stats'][4]['base_stat'],
                'speed': data['stats'][5]['base_stat'],
            },
            'moves': build_moves(data['moves'])
        }
        return pokemon
    else:
        return None
