import  requests, random

base_URL="https://pokeapi.co/api/v2/pokemon/"
pokemon={ 1:"bulbasaur", 4:"charmander", 7:"squirtle" }


def get_pokemon(id):
    URL=base_URL+str(id)
    response=requests.get(URL)
    data=response.json()
    chosenMoves=[]
    moves = data["moves"]
    while len(chosenMoves) < 4:
        randomIndex=random.randint(0,len(moves))
        move=moves[randomIndex]["move"]["name"]
        if move not in chosenMoves:
            chosenMoves.append(move)

    for type in data["types"]:
        print(type)
    print(chosenMoves)
    return chosenMoves

def find_pokemon(name):
    url = None
    searches = 0
    while searches < 8:
        response = None
        if (url):
            response = requests.get(url)
        else:
            response = requests.get(base_URL)

        data = response.json()

        for pokemon in data['results']:
            if pokemon['name'] == name: 
                return pokemon['url'].replace(base_URL, '').replace('/', '')

        url = data['next']
        searches += 1
        
    return None
