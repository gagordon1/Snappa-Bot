from tabulate import tabulate

def generate_leaderboard_string(data: list):
    """Generates a leaderboard string given a list of player data

    Parameters
    ----------
    data : [[name : str, ELO : float, number of wins : int, number of losses : int]]

    Returns
    -------
    String
        A string of leaderboards matching the format described in messages.txt

    """
    return tabulate(data, headers = ["Name", "ELO", "Wins", "Losses"])


if __name__ == '__main__':
    data = [['Garrett Gordon', 69.1, 5, 6], ['Andrei Dumitrescu', 69.3, 4, 9]]
    out = generate_leaderboard_string(data)
    print(out)
