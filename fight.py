from processors import party_parser
from file_operations import read_file, save_file, update_file
from api import calculate_stat, calculate_health
import random, ast

def get_temp(userId, opponentId):
    temp = read_file('temp.txt')

    for line in temp:
        split_line = line.split('[:]')

        if (str(userId) == split_line[0] and str(opponentId) == split_line[3]
        ) or (str(userId) == split_line[3] and str(opponentId) == split_line[0]):
            return temp_parser(line)
    
    return None

def save_temp(userId, speed, effect, opponentId):
    temp = read_file('temp.txt')

    temp.append(f'{userId}[:]{speed}[:]{effect}[:]{opponentId}') 

    save_file('temp.txt', temp)       

def temp_parser(temp):
    split_temp = temp.split('[:]')

    return {
        'userId': split_temp[0],
        'speed': split_temp[1],
        'effects': ast.literal_eval(split_temp[2]),
        'opponentId': split_temp[3],
    }    

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

def delete(userId, opponentId):
    duels=read_file("duels.txt")
    file=[]
    for d in duels:
        splitDuel=d.split("[:]")
        if splitDuel[0] != (str(userId) or str(opponentId)) and splitDuel[2] != (str(userId) or str(opponentId)):
            file.append(d)
    save_file("duels.txt",file)

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
        save_temp(userId,0,[],defenderId)
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
    damage=-round(((((((2*attackerLevel)/5)+2)*rightHalf)/50)+2)*finalModifier, 2)
    print("Took", damage,"points of damage")
    print(move["pp"])
    effects.append({
        "action": "hp",
        "target":"opponent",
        "change":damage
    })
    speed= attacker["stats"]["speed"]
    var=get_temp(userId,defenderId)
    moveList=""
    if var is not None:
        if int(speed) > int(var["speed"]):
            for effect in effects:
                if effect["target"] == "self":
                    if effect["action"] in attacker["stats"]:
                        attacker["stats"][effect["action"]] += round(effect["change"], 2)
                    else:
                        move[effect["target"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{userId}> increased their {effect["action"]} by {effect["change"]}\n'
                else:
                    if effect["action"] in defender["stats"]:
                        defender["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{userId}> decreased <@!{defenderId}>\'s {effect["action"]} by {effect["change"]}\n'
            for effect in var["effects"]:
                if effect["target"] == "self":
                    if effect["action"] in defender["stats"]:
                        defender["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{defenderId}> increased their {effect["action"]} by {effect["change"]}\n'
                else:
                    if effect["action"] in attacker["stats"]:
                        attacker["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{defenderId}> decreased <@!{userId}>\'s {effect["action"]} by {effect["change"]}\n'
        else:
            for effect in var["effects"]:
                if effect["target"] == "self":
                    if effect["action"] in defender["stats"]:
                        defender["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{defenderId}> increased their {effect["action"]} by {effect["change"]}\n'
                else:
                    if effect["action"] in attacker["stats"]:
                        attacker["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{defenderId}> decreased <@!{userId}>\'s {effect["action"]} by {effect["change"]}\n'
            for effect in effects:
                if effect["target"] == "self":
                    if effect["action"] in attacker["stats"]:
                        attacker["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{userId}> increased their {effect["action"]} by {effect["change"]}\n'
                else:
                    if effect["action"] in defender["stats"]:
                        defender["stats"][effect["action"]] += round(effect["change"], 2)
                    moveList=moveList+ f'<@!{userId}> decreased <@!{defenderId}>\'s {effect["action"]} by {effect["change"]}\n'
        temp = read_file('temp.txt')

        file = []
        for t in temp:
            split_temp = t.split('[:]')
            if split_temp[0] != (str(userId) or str(defenderId)) and split_temp[3] != (str(userId) or str(defenderId)):
                file.append(t)

        save_file('temp.txt', file)
    else:
        save_temp(userId,speed,effects,defenderId)
        return "mover recorded good sir"

    update_file("duels.txt",f'{userId}[:]{attacker}[:]{defenderId}[:]{defender}[:]{attackerLevel}')

    if int(attacker["stats"]["hp"]) <= 0:
        moveList = moveList + f'<@!{userId}> fainted! <@!{defenderId}> is the winner with {defender["stats"]["hp"]} remaining!!'
        delete(userId,defenderId)
    elif int(defender["stats"]["hp"]) <= 0:
        moveList = moveList + f'<@!{defenderId}> fainted! <@!{userId}> is the winner with {attacker["stats"]["hp"]} remaining!!'
        delete(userId,defenderId)
    else:
        moveList=moveList+f'<@!{userId}>\'s health is {attacker["stats"]["hp"]} and <@!{defenderId}>\'s health is {defender["stats"]["hp"]}'
    return moveList

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

