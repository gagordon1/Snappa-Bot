import pygsheets

SERVICE_FILE = 'google_keys/spartan-matter-323500-b7144290e762.json'
SPREADSHEET_NAME = "Snappa Database"
PLAYER_SHEET_DATA_RANGE = "B2:E500"
PLAYER_NAME_COLUMN = 2
DEFAULT_ELO = 1500
DEFAULT_WINS = 0
DEFAULT_LOSSES = 0

class GoogleSheetsDatabase:
    def __init__(self, player_sheet_index, game_sheet_index):
        gc = pygsheets.authorize(service_file=SERVICE_FILE)
        self.sh = gc.open(SPREADSHEET_NAME)
        self.player_wks = self.sh.worksheets()[player_sheet_index]
        self.game_wks = self.sh.worksheets()[game_sheet_index]

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
        player_column = self.player_wks.get_col(PLAYER_NAME_COLUMN)
        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            player_column)]
        if player not in players:
            return "Player {} does not exist in the database!".format(player)
        row = 1 + player_column.index(player)
        data_start_column = 2
        data_end_column = 5
        return [int(x) for x in self.player_wks.get_row(row)[data_start_column:data_end_column]]

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
        player_column = self.player_wks.get_col(PLAYER_NAME_COLUMN)
        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            player_column)]
        if player not in players:
            return "Player {} does not exist in the database!".format(player)
        row = 1 + player_column.index(player)
        crange = "C{}:E{}".format(row, row)
        self.player_wks.update_values(crange = crange, values = [[ELO, number_of_wins, number_of_losses]])
        return "Player data successfully updated!"


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
        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            self.player_wks.get_col(PLAYER_NAME_COLUMN))]
        for player in [player1, player2, player3, player4]:
            if player not in players:
                return "Player {} does not exist in the database!".format(player)

        next_row = self.get_next_open_row(self.game_wks)
        crange = "B{}:H{}".format(next_row, next_row)
        self.game_wks.update_values(crange = crange, values = [[timestamp, player1, player2,
            player3, player4, team_1_score, team_2_score]])
        return "Game successfully logged!"

    def get_leaderboard(self):
        """Gets all player data from the leaderboard

        Returns
        -------
        [[name, ELO, number of wins, number of losses]]
            List of lists containing each player's data

        """
        i = 3
        j = self.get_next_open_row(self.player_wks)
        out = []
        for ind in range(i,j):
            row = self.player_wks.get_row(ind)[1:5]
            out.append([row[0], int(row[1]),int(row[2]),int(row[3])])
        return out






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
        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            self.player_wks.get_col(PLAYER_NAME_COLUMN))]
        if name in players:
            #name already in database
            return "Player already exists in the database!"
        else:
            row = self.get_next_open_row(self.player_wks)
            crange = "B{}:E{}".format(row, row)
            self.player_wks.update_values(crange = crange, values = [[name, DEFAULT_ELO,
                DEFAULT_WINS, DEFAULT_LOSSES]])
            return "Player {} successfully added!".format(name)


    def get_next_open_row(self, wks):
        i = 3
        while any(elt != '' for elt in wks.get_row(i)[1:10]):
            i += 1
        return i
