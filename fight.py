from processors import party_parser
from file_operations import read_file
import random

#userId:{pokemon:health}|opponentId:{pokemon:health}
#475134908206153728:squirtle:7:['dig', 'facade', 'yawn', 'brine']:


def duel(userId, opponentId):
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
    return "Duel!"



def executeMove(moveText,attackerId,userId):
    attacker=duel()
    defender=duel()
    move=None
    moves=attacker["moves"]
    for m in moves:
        if moveText == m["name"]:
            move=m
    if move is None:
        return "That is not a valid move, fool"
    accuracy=move["accuracy"]
    power= move["power"]
    moveType=move["type"]
    randomAttackDamage=(random.randint(85,100))/100
    attackerLevel=attacker["level"]
    attackingStat=attacker["stats"]["attack"]
    specialAttackingStat=attacker["stats"]["special-attack"]

    defendingAttack=defender["stats"]["defense"]
    defendingSpecialAttack=defender["stats"]["special-defense"]


    damageType=move["damage_class"]["type"]
    if damageType=="status":

        statChange=move["stat_changes"]["change"]
        statThatChanges=move["stat_changes"]["name"]
        if statChange > 0:
            statusMove(attacker,statChange,statThatChanges)
        if statChange<0:
            statusMove(defender,statChange,statThatChanges)
    elif damageType=="physical":
        attacking(attackingStat, defendingAttack)
    elif damageType=="special":
        attacking(specialAttackingStat, defendingSpecialAttack)


def attacking(offensive,defensive):
    pass
def statusMove(effectedPokemon,move,statThatChanges):
    pass