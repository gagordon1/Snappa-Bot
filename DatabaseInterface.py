
class Database:

    def get_player_data(self, player : str):
        """Gets ELO, number of wins and number of losses for a player

        Parameters
        ----------
        player : str
            Name of the player

        Returns
        -------
        [int]
            List of [ELO, number of wins, number of losses]

        """
        pass

    def updatePlayerData(self, player : str, ELO : int,
        number_of_wins : int, number_of_losses : int):
        """Updates data at a player's column

        Parameters
        ----------
        player : str
            name of the player
        ELO : int
            new ELO to be logged
        number_of_wins : int
            new number of wins to be logged
        number_of_losses : int
            new number of losses to be logged

        Returns
        -------
        str
            message saying if data was updated or not

        """
        pass

    def log_game(self, timestamp : int,
            player1 : str,
            player2 : str,
            player3 : str,
            player4 : str,
            team_1_score : int,
            team_2_score : int):
        """Logs a game in the database.

        Parameters
        ----------
        timestamp : int
            unix epoch time in seconds of the game.
        player1 : str
            One of the team 1 players.
        player2 : str
            The other team 1 player.
        player3 : str
            One of the team 2 players.
        player4 : str
            The other team 2 player.
        team_1_score : int
            Team 1's score.
        team_2_score : int
            Team 2's score.

        Returns
        -------
        type
            Message saying if the score was properly logged or not.

        """
        pass

    def get_leaderboard(self):
        """Gets all player data from the leaderboard

        Returns
        -------
        [[name, ELO, number of wins, number of losses]]
            List of lists containing each player's data

        """
        pass



    def add_player(self, name : str):
        """Adds a player to the google sheet database

        Parameters
        ----------
        name : str
            Name of the player to add

        Returns
        -------
        type
            Message declaring if the player was added or not

        """
        pass
