from SnappaLeaderboardTextGenerator import generate_leaderboard_string
from tabulate import tabulate

class SnappaLeaderboard:

    def __init__(self, database):
        self.database = database

    def get_player_history(self, name : str):
        """Gets the history of a player's snappa games

        Parameters
        ----------
        name : String
            Name of the player

        Returns
        -------
        String
            A list of the player's snappa games

        """
        pass

    def get_leaderboard(self, n : int):
        """Get the top n players in the leaderboard along with their overall
        record

        Parameters
        ----------
        n : int
            Number of players to return

        Returns
        -------
        String
            The top n players in the leaderboard along with their record

        """
        try:
            entries = self.database.get_leaderboard()
            return generate_leaderboard_string(entries, n)
        except Exception:
            return "Leaderboard could not be accessed!".format(name)



    def add_player(self, name : str):
        """Add a player to the leaderboard system

        Parameters
        ----------
        name : String
            name of the user

        Returns
        -------
        String
            Message describing if the player was added correctly or not

        """
        try:
            self.database.add_player(name)
            return "Player {} successfully added to the database!".format(name)
        except Exception:
            return "Player {} could not be added to the database!".format(name)



    def log_score(self, winner1 : str,
        winner2 :str,
        loser1 : str,
        loser2 : str,
        winner_score : int,
        loser_score : int):
        """Log a game to the system

        Returns
        -------
        String
            Message showing the result of the outcome of a snappa game

        """
        pass


    def generate_message(self):
        """Generates a randomly chosen message

        Returns
        -------
        String
            Randomly chosen message from a set of phrases

        """
        pass

if __name__ == '__main__':
    pass
