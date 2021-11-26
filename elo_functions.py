from elosports.elo import Elo
K = 20

def calculate_elo_change(winner1, w_elo_1, winner2, w_elo_2, loser1, l_elo_1, loser2, l_elo_2):
    elo = Elo(k = K)
    winner_avg_score = (w_elo_1 + w_elo_2) /2
    loser_avg_score = (l_elo_1 + l_elo_2) /2
    result = elo.expectResult(winner_avg_score, loser_avg_score)

    elo_change = K*(1-result)
    return int(elo_change)

if __name__ == '__main__':

    # elo = Elo(k = K)
    # elo.addPlayer("Garrett", rating = 1500)

    # elos = {"Garrett" : 1500, "Andrei" :1500, "Noah" :1500, "Sebastian" :1500}
    #
    # delta = calculate_elo_change("Garrett", "Andrei", "Noah", "Sebastian")
    # print(delta)
    pass
