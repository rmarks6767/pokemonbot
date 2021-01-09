from processors import party_parser
from file_operations import read_file

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





