from tabulate import tabulate

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
    return tabulate(data_sorted, headers = ["Rank","Name", "ELO", "Wins", "Losses"])

def generate_score_log_string(data : list):
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
    return tabulate(data, headers = ["Name", "New Rank", "New ELO", "ELO Change"])

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
    return tabulate([[player] + [rank] + data], headers = ["Name", "Rank", "ELO", "Wins", "Losses"])



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
