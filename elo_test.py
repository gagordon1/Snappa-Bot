from elosports.elo import Elo

K = 20
elo = Elo(k = K)
# elo.addPlayer("Garrett", rating = 1500)

elos = {"Garrett" : 1500, "Andrei" :1500, "Noah" :1500, "Sebastian" :1500}

def get_elo(player):
    return elos[player]

def calculate_elo_change(winner1, winner2, loser1, loser2):
    winner_avg_score = (get_elo(winner1) + get_elo(winner2)) /2
    loser_avg_score = (get_elo(loser1) + get_elo(loser2)) /2
    result = elo.expectResult(winner_avg_score, loser_avg_score)

    elo_change = K*(1-result)
    return int(elo_change)



delta = calculate_elo_change("Garrett", "Andrei", "Noah", "Sebastian")
print(delta)
