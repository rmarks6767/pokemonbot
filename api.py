import  requests, random

base_URL="https://pokeapi.co/api/v2/pokemon/"
pokemon={ 1:"bulbasaur", 4:"charmander", 7:"squirtle" }


def get_pokemon():

    for i in pokemon.keys():
        URL=base_URL+str(i)
        print(URL)
        response=requests.get(URL)
        data=response.json()
        #print(data)
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

