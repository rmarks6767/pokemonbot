import  requests, random

base_URL="https://pokeapi.co/api/v2/pokemon/"

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
    response = requests.get(base_URL + name)
    data = response.json()

    if data != None:
        return data['id']
    else:
        return None
