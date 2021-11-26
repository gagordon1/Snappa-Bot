from SnappaLeaderboardTextGenerator import generate_leaderboard_string, generate_score_log_string
from elo_functions import calculate_elo_change
from tabulate import tabulate
from Databases.MessageDatabase import messages
import random
import time

class SnappaLeaderboard:

    def __init__(self, database, k = 20):
        self.database = database
        self.k = k

    def get_elo(self, name):
        try:
            elo = self.database.get_player_data(name)[0]
            return int(elo)
        except:
            return -1

    def get_ranks(self, players):
        """Gets ranks of players sorted by ELO then alphabetically
        Parameters
        ----------
        players : [str]
            list of player names

        Returns
        -------
        {str : int}
            Dictionary mapping players to their rank in the leaderboard

        """
        leaderboard = self.database.get_leaderboard()
        filtered = [x for x in filter(lambda elt : elt[0] in players,leaderboard)]
        ordered = sorted(sorted(filtered, key = lambda x : x[0].lower()),
                key = lambda x: x[1], reverse = True)
        out = {}
        i = 1
        for entry in ordered:
            out[entry[0]] = i
            i += 1
        return out

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



    def add_player(self, name : str, initial_elo :int, initial_wins : int, initial_losses :int):
        """Add a player to the leaderboard system

        Parameters
        ----------
        name : String
            name of the user
        initial_elo : int
            Initial elo of the player
        initial_wins : int
            Initial number of wins for the player
        initial_losses : int
            Initial number of losses for the player

        Returns
        -------
        String
            Message describing if the player was added correctly or not

        """
        try:
            self.database.add_player(name, initial_elo, initial_wins, initial_losses)
            return "Player {} successfully added to the database!".format(name)
        except Exception:
            return "Player {} could not be added to the database!".format(name)


    def set_k(self, k : int):
        """Updates the k value for the elo calculation

        Parameters
        ----------
        k : int
            k value for elo calculation

        """
        self.k = k

    def get_k(self):
        return self.k


    def log_score(self, player1 : str,
        player2 :str,
        player3 : str,
        player4 : str,
        team_1_score : int,
        team_2_score : int):
        """Log a game to the system

        Returns
        -------
        String
            Message showing the result of the outcome of a snappa game

        """

        t = time.time()
        self.database.log_game(t, player1, player2, player3, player4, team_1_score, team_2_score)
        if team_1_score > team_2_score:
            winner1 = player1
            winner2 = player2
            loser1 = player3
            loser2 = player4
        else:
            loser1 = player1
            loser2 = player2
            winner1 = player3
            winner2 = player4

        elo_change = calculate_elo_change(winner1, self.get_elo(winner1),
                                winner2, self.get_elo(winner2),
                                loser1, self.get_elo(loser1),
                                loser2, self.get_elo(loser2),
                                self.k
                            )

        out = []
        for player in [winner1, winner2]:
            # elo, wins, losses = self.database.get_player_data(player)
            obj = self.database.get_player_data(player)
            elo = obj[0]
            wins = obj[1]
            losses = obj[2]
            new_elo = elo + elo_change
            out.append([player, new_elo, elo_change])

            self.database.updatePlayerData(player, new_elo, wins + 1, losses)

        for player in [loser1, loser2]:
            # elo, wins, losses = self.database.get_player_data(player)
            obj = self.database.get_player_data(player)
            elo = obj[0]
            wins = obj[1]
            losses = obj[2]
            new_elo = elo - elo_change
            out.append([player, new_elo, -elo_change])
            self.database.updatePlayerData(player, new_elo, wins, losses + 1)

        #insert new rank
        ranks = self.get_ranks([winner1, winner2, loser1, loser2])
        for entry in out:
            name = entry[0]
            entry.insert(1, ranks[name])

        # "Game could not be logged!".format(name)
        return generate_score_log_string(out)



    def generate_message(self):
        """Generates a randomly chosen message

        Returns
        -------
        String
            Randomly chosen message from a set of phrases

        """
        return random.choice(messages)

if __name__ == '__main__':
    # slb = SnappaLeaderboard()
    pass
