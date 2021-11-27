
LINE_WIDTH = 26
LEADERBOARD_WIDTH = 34

def generate_leaderboard_string(data: list, n : int):
    """Generates a leaderboard string given a list of player data

    Parameters
    ----------
    n : int
        number of entries to return

    data : [[name : str, ELO : float, number of wins : int, number of losses : int]]
        Player data
    Returns
    -------
    String
        A string of leaderboards matching the format described in messages.txt

    """
    data_sorted = sorted(data, key = lambda x : x[1], reverse = True)[:n] #sort on ELO
    i = 1
    for entry in data_sorted:
        rank = i
        entry.insert(0, rank)
        i += 1

    leaderboard_title = "SNAPPA LEADERBOARD"
    x = int((LEADERBOARD_WIDTH - len(leaderboard_title))/2)
    out_string = "="*x +leaderboard_title + "="*x +"\n"+ "-"*LEADERBOARD_WIDTH +"\n"

    for entry in data_sorted:
        rank, name, ELO, w, l = entry
        out_string += "{}. {} {} ({}-{})\n".format(rank, ELO, name, w, l)
    return out_string


def generate_score_log_string(data : list, score_1 : int, score_2 : int):
    """Gets the log string after a game

    Parameters
    ----------
    data : list
        list of list of data : [[Name, New Rank, New ELO, ELO Change]]

    Returns
    -------
    str
        Tabulated version of this information

    """
    out_string = "Score Logged. {}-{}\n".format(score_1, score_2)
    out_string += "-"*LINE_WIDTH +"\n"
    for d in data:
        name = d[0]
        elo_change = d[3]
        new_rank = d[1]
        if elo_change >= 0:
            out_string += "{}. {} +{}\n".format(new_rank, name, elo_change)
        else:
            out_string += "{}. {} {}\n".format(new_rank, name, elo_change)
    out_string += "-"*LINE_WIDTH
    return out_string

def generate_player_data_string(player : str, rank : int, data : list):
    """Gets player data as a tabulated string

    Parameters
    ----------
    data : list
        list of player data  [ELO, number of wins, number of losses]

    Returns
    -------
    str
        Tabulated version of the player data

    """
    out_string = "Player {}:\n".format(player)
    out_string += "-"*LEADERBOARD_WIDTH +"\n"
    out_string += "Rank: {} ELO: {} Record: {}-{}\n".format(rank, *data)
    out_string += "-"*LEADERBOARD_WIDTH +"\n"
    return out_string



if __name__ == '__main__':
    # data = [['Garrett Gordon', 701, 5, 6], ['Andrei Dumitrescu', 700, 4, 9]]
    # out = generate_leaderboard_string(data)
    # print(out)
    data = [
        ["Garrett", 2, 1510, 10],
        ["Andrei", 1, 1510, 10],
        ["Noah", 3, 1490, -10],
        ["Sebastian", 4, 1490, -10]
    ]
    out = generate_score_log_string(data)
    print(out)
