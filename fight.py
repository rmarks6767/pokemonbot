from processors import party_parser
from file_operations import read_file
import random, ast

#userId:{pokemon:health}|opponentId:{pokemon:health}
#475134908206153728:squirtle:7:['dig', 'facade', 'yawn', 'brine']:

def duel_parser(duel):
    split_duel = duel.split('[:]')

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

    duels= read_file(duels.txt)
    for duel in duels:
        split_duel = duel.split('[:]')
        if (split_duel[0] == str(userId)) and split_duel[2] == str(opponentId):
            return "You already got a battle with this fella!"

    return "Duel!"



def executeMove(moveText,defenderId,userId):
    duels=read_file("duels.txt")
    for d in duels:
        duel=duel_parser(d)
        if duel["userId"]==userId:
            attacker=duel["pokemon"]
        elif duel["userId"]==defenderId:
            defender=duel["pokemon"]
    move=None
    moves=attacker["moves"]
    for m in moves:
        if moveText == m["name"]:
            move=m
    if move is None:
        return "That is not a valid move, fool"
    if move["pp"] == 0:
        return f"<@!{userId}> has no pp, zero"

    accuracy=move["accuracy"]

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
    if damageType=="status":

        statChange=move["stat_changes"]["change"]
        statThatChanges=move["stat_changes"]["name"]
        if statChange > 0:
            statusMove(attacker,statChange,statThatChanges)
        elif statChange<0:
            statusMove(defender,statChange,statThatChanges)
        move["pp"]= int(move["pp"])-1 #Update
        return "Did " + move["name"]+". "

    elif damageType=="physical":
        rightHalf=rightHalfEquation(attackingStat, defendingAttack,power)
    elif damageType=="special":
        rightHalf=rightHalfEquation(specialAttackingStat, defendingSpecialAttack,power)
    finalModifier=modifier(moveType,attackerTypeList,(random.randint(85,100))/100,move["damage_class"]["relations"], defendingTypesList)
    damage=((((((2*attackerLevel)/5)+2)*rightHalf)/50)+2)*finalModifier
    print("Took", damage,"points of damage")
    print(defender)
    defender["stats"]["hp"]=defender["stats"]["hp"]-damage #Update



def rightHalfEquation(offensive,defensive,power):
    rightHalf= power * (offensive/defensive)
    return rightHalf
def statusMove(effectedPokemon,move,statThatChanges):
    effectedPokemon[statThatChanges]=move + int(effectedPokemon[statThatChanges]) #Update

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

