from elosports.elo import Elo

def calculate_elo_change(winner1, w_elo_1, winner2, w_elo_2, loser1, l_elo_1, loser2, l_elo_2, k):
    elo = Elo(k = k)
    winner_avg_score = (w_elo_1 + w_elo_2) /2
    loser_avg_score = (l_elo_1 + l_elo_2) /2
    result = elo.expectResult(winner_avg_score, loser_avg_score)

    elo_change = k*(1-result)
    return int(elo_change)
