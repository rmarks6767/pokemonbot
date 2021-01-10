from processors import party_parser
from file_operations import read_file, save_file
from api import calculate_stat, calculate_health
import random, ast


def duel_parser(d):
    split_duel = d.split('[:]')

    return {
        'userId': split_duel[0],
        'userPokemon': ast.literal_eval(split_duel[1]),
        'opponentId': split_duel[2],
        'opponentPokemon': ast.literal_eval(split_duel[3]),
        'level': split_duel[4],
    }

def duel(userId, opponentId, level):
    if userId == opponentId:
        return "You cant duel yourself, stupid, dumb, white, idiot"
    parties=read_file("parties.txt")
    userParty=None
    opponentParty=None
    for p in parties:
        party=party_parser(p)
        if party["userId"] == userId:
            userParty=party
        elif party["userId"] == opponentId:
            opponentParty = party
    print(userParty)
    if userParty is None:
        return f'<@!{userId}>, you do not have a party'
    elif opponentParty is None:
        return f"<@!{opponentId}>, you do not have a party"

    duels= read_file('duels.txt')
    for d in duels:
        split_duel = d.split('[:]')
        if (split_duel[0] == str(userId)) and split_duel[2] == str(opponentId):
            return "You already got a battle with this fella!"

    userParty['pokemon']['stats'] = {
        'hp': calculate_health(userParty['pokemon']['stats']['hp'], level),
        'attack': calculate_stat(userParty['pokemon']['stats']['attack'], level),
        'defense': calculate_stat(userParty['pokemon']['stats']['defense'], level),
        'special-attack': calculate_stat(userParty['pokemon']['stats']['special-attack'], level),
        'special-defense': calculate_stat(userParty['pokemon']['stats']['special-defense'], level),
        'speed': calculate_stat(userParty['pokemon']['stats']['speed'], level),
    }

    opponentParty['pokemon']['stats'] = {
        'hp': calculate_health(opponentParty['pokemon']['stats']['hp'], level),
        'attack': calculate_stat(opponentParty['pokemon']['stats']['attack'], level),
        'defense': calculate_stat(opponentParty['pokemon']['stats']['defense'], level),
        'special-attack': calculate_stat(opponentParty['pokemon']['stats']['special-attack'], level),
        'special-defense': calculate_stat(opponentParty['pokemon']['stats']['special-defense'], level),
        'speed': calculate_stat(opponentParty['pokemon']['stats']['speed'], level),
    }

    duels.append(f'{userId}[:]{userParty["pokemon"]}[:]{opponentId}[:]{opponentParty["pokemon"]}[:]{level}')

    save_file("duels.txt",duels)

    return "Duel!"



def executeMove(moveText,defenderId,userId):
    duels=read_file("duels.txt")
    defender=None
    attacker=None

    effects=[]

    for d in duels:
        selected_duel=duel_parser(d)
        if selected_duel["userId"]==userId and selected_duel["opponentId"]== defenderId:
            attacker=selected_duel["userPokemon"]
            defender=selected_duel["opponentPokemon"]
        elif selected_duel["userId"]==defenderId and selected_duel["opponentId"]== userId:
            attacker=selected_duel["opponentPokemon"]
            defender=selected_duel["userPokemon"]
    move=None
    moves=attacker["moves"]
    for m in moves:
        print (m["name"])
        if moveText == m["name"]:
            move=m
    if move is None:
        return "That is not a valid move, fool"
    if move["pp"] == 0:
        return f"<@!{userId}> has no pp, zero"

    move["pp"] = int(move["pp"]) - 1
    accuracy = move["accuracy"]

    if random.randint(0, 100) >= accuracy:
        return "You missed your attack"


    power= move["power"]
    moveType=move["type"]
    attackerLevel=attacker["level"]
    attackingStat=attacker["stats"]["attack"]
    specialAttackingStat=attacker["stats"]["special-attack"]
    attackerTypeList=attacker["types"]

    defendingAttack=defender["stats"]["defense"]
    defendingSpecialAttack=defender["stats"]["special-defense"]
    defendingTypesList=defender["types"]


    damageType=move["damage_class"]["type"]
    rightHalf=None

    for element in move["stat_changes"]:
        statChange = element["change"]
        if statChange > 0:
            effects.append({
                "action":element["name"],
                "target": "self",
                "change": statChange
            })
            #statusMove(attacker,statChange,element["name"])
        elif statChange<0:
            effects.append({
                "action": element["name"],
                "target": "opponent",
                "change": statChange
            })
            # statusMove(attacker,statChange,element["name"])
    if damageType=="status":
        return "You did status"
    if damageType=="physical":
        rightHalf=rightHalfEquation(attackingStat, defendingAttack,power)
    elif damageType=="special":
        rightHalf=rightHalfEquation(specialAttackingStat, defendingSpecialAttack,power)
    finalModifier=modifier(moveType,attackerTypeList,(random.randint(85,100))/100,move["damage_class"]["relations"], defendingTypesList)
    print(attackerLevel,rightHalf,finalModifier)
    damage=((((((2*attackerLevel)/5)+2)*rightHalf)/50)+2)*finalModifier
    print("Took", damage,"points of damage")
    print(move["pp"])
    effects.append({
        "action": "hp",
        "target":"opponent",
        "change":damage
    })



    #defender["stats"]["hp"]=defender["stats"]["hp"]-damage #Update
    return defender["stats"]["hp"]

def rightHalfEquation(offensive,defensive,power):
    print(power,offensive,defensive)
    rightHalf= power * (offensive/defensive)
    return rightHalf
def statusMove(effectedPokemon,move,statThatChanges):
    effectedPokemon["stats"][statThatChanges]=move + int(effectedPokemon["stats"][statThatChanges]) #Update

def modifier(moveType,attackerTypeList,randMult,moveRelationsTo,defendingTypeList):
    if moveType in attackerTypeList:
        STAB=1.5
    else:
        STAB=1
    relationsMultiplier=relations(moveRelationsTo, defendingTypeList)
    return randMult*STAB*relationsMultiplier

def relations(moveRelationsTo,defendingTypeList):
    base=1
    for defendingType in defendingTypeList:
        if defendingType in moveRelationsTo["double_damage_to"]:
            base=base*2
        elif defendingType in moveRelationsTo["half_damage_to"]:
            base=base*.5
        elif defendingType in moveRelationsTo["no_damage_to"]:
            base=base*0
    return base

