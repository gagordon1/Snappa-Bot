from SnappaLeaderboardTextGenerator import generate_leaderboard_string, generate_score_log_string
from SnappaLeaderboardTextGenerator import generate_player_data_string
from HelperFunctions.elo_functions import calculate_elo_change
from tabulate import tabulate
from Databases.MessageDatabase import messages
import random
import time

MAX_NAME_LENGTH = 30

class SnappaLeaderboard:

    def __init__(self, database, k = 20):
        self.database = database
        self.k = k

    def get_elo(self, name):
        try:
            elo = self.database.get_player_data(name)[0]
            return int(elo)
        except:
            raise Exception("Database could not be accessed!")

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

        Throws
        ------
        Exception
            throws an exception if database could not be accessed

        """
        try:
            leaderboard = self.database.get_leaderboard()
        except:
            raise Execption("Database could not be accessed!")

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

        Throws
        ------
        Exception
            throws an exception if leaderboard could not be accessed

        """
        try:
            entries = self.database.get_leaderboard()
            return generate_leaderboard_string(entries, n)
        except:
            raise Exception("Database could not be accessed!")



    def add_player(self, name : str, initial_elo :int, initial_wins : int, initial_losses :int):
        """Add a player to the leaderboard system

        Parameters
        ----------
        name : String
            name of the user (cannot be '' and cannot be longer than
            30 characters and already exist in the system)
        initial_elo : int
            Initial elo of the player
        initial_wins : int
            Initial number of wins for the player
        initial_losses : int
            Initial number of losses for the player

        Throws
        ------
        Exception
            throws an exception if player is not successfully added

        """
        if len(name) > MAX_NAME_LENGTH:
            raise Exception("Player {}'s name is too long!").format(name)
        elif name == '':
            raise Exception("Player's name cannot be empty!")
        response = self.database.add_player(name, initial_elo, initial_wins, initial_losses)
        if response != "Player {} successfully added!".format(name):
            raise Exception(response)

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

    def get_rank(self, player : str):
        return self.get_ranks([player])[player]

    def get_player_data(self, player):
        """Gets player data

        Parameters
        ----------
        player : str
            Name of the player

        Returns
        -------
        str
            tabulated data with name, rank, elo, wins, losses

        """
        try:
            rank = self.get_rank(player)
            data = self.database.get_player_data(player)
            return generate_player_data_string(player, rank, data)
        except:
            raise Exception("Player data could not be accessed!")



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

        Throws
        ------
        Exception
            throws an exception if game is not successfully logged
        """

        t = int(time.time())
        try:
            response = self.database.log_game(t, player1, player2, player3, player4, team_1_score, team_2_score)
        except:
            raise Exception("Game could not be logged!")

        if response != "Game successfully logged!":
            raise Exception(response)

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
        try:
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
        except:
            raise Exception("Player data could not be accessed!")

        #insert new rank
        ranks = self.get_ranks([winner1, winner2, loser1, loser2])
        for entry in out:
            name = entry[0]
            entry.insert(1, ranks[name])


        return generate_score_log_string(sorted(out, key = lambda x : x[1]), team_1_score, team_2_score) #sort on rank



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
