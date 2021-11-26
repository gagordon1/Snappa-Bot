import pygsheets

SERVICE_FILE = 'google_keys/spartan-matter-323500-b7144290e762.json'
SPREADSHEET_NAME = "Snappa Database"
PLAYER_SHEET_DATA_RANGE = "B2:E500"
PLAYER_NAME_COLUMN = 2
PLAYER_SHEET_TEST_INDEX = 2
GAME_SHEET_TEST_INDEX = 3
PLAYER_SHEET_INDEX = 0
GAME_SHEET_INDEX = 1
START_OF_DATA = "B3"

class GoogleSheetsDatabase:
    def __init__(self, test = False):
        gc = pygsheets.authorize(service_file=SERVICE_FILE)
        self.sh = gc.open(SPREADSHEET_NAME)
        if test:
            #clear sheets
            self.player_wks = self.sh.worksheets()[PLAYER_SHEET_TEST_INDEX]
            self.game_wks = self.sh.worksheets()[GAME_SHEET_TEST_INDEX]
            self.initialize_game_log()
            self.initialize_player_sheet()
        else:
            self.player_wks = self.sh.worksheets()[PLAYER_SHEET_INDEX]
            self.game_wks = self.sh.worksheets()[GAME_SHEET_INDEX]


    def initialize_game_log(self):
        self.game_wks.clear(start = START_OF_DATA)

    def initialize_player_sheet(self):
        self.player_wks.clear(start = START_OF_DATA)

    def get_player_games(self, name : str):
        i = 3
        j = self.get_next_open_row(self.game_wks)
        out = []
        names_start_index = 2
        names_end_index = 6
        game_start_index = 1
        game_end_index = 8
        for ind in range(i,j):
            row = self.game_wks.get_row(ind, include_tailing_empty = False)
            names = row[names_start_index:names_end_index]
            if name in names:
                out.append(self.process_game_from_sheets(row[game_start_index:game_end_index]))
        return out

    def process_game_from_sheets(self, game):
        out = game[:]
        out[0] = int(game[0])
        out[5] = int(game[5])
        out[6] = int(game[6])
        return out


    def get_player_data(self, player : str):
        player_column = self.player_wks.get_col(PLAYER_NAME_COLUMN, include_tailing_empty = False)
        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            player_column)]
        if player not in players:
            return "Player {} does not exist in the database!".format(player)
        row = 1 + player_column.index(player)
        data_start_column = 2
        data_end_column = 5
        ret = [int(x) for x in self.player_wks.get_row(row, include_tailing_empty = False)[data_start_column:data_end_column]]
        return ret

    def updatePlayerData(self, player : str, ELO : int,
        number_of_wins : int, number_of_losses : int):
        player_column = self.player_wks.get_col(PLAYER_NAME_COLUMN , include_tailing_empty = False)
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
        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            self.player_wks.get_col(PLAYER_NAME_COLUMN, include_tailing_empty = False))]
        for player in [player1, player2, player3, player4]:
            if player not in players:
                return "Player {} does not exist in the database!".format(player)

        next_row = self.get_next_open_row(self.game_wks)
        crange = "B{}:H{}".format(next_row, next_row)
        self.game_wks.update_values(crange = crange, values = [[timestamp, player1, player2,
            player3, player4, team_1_score, team_2_score]])
        return "Game successfully logged!"

    def get_leaderboard(self):
        i = 3
        j = self.get_next_open_row(self.player_wks)
        out = []
        for ind in range(i,j):
            row = self.player_wks.get_row(ind, include_tailing_empty = False)[1:5]
            out.append([row[0], int(row[1]),int(row[2]),int(row[3])])
        return out


    def add_player(self, name : str, initial_elo :int, initial_wins : int, initial_losses : int):

        players = [p for p in filter(lambda x : (x != '' and x != 'Name'),
            self.player_wks.get_col(PLAYER_NAME_COLUMN, include_tailing_empty = False))]
        if name in players:
            #name already in database
            return "Player already exists in the database!"
        else:
            row = self.get_next_open_row(self.player_wks)
            crange = "B{}:E{}".format(row, row)
            self.player_wks.update_values(crange = crange, values = [[name, initial_elo,
                initial_wins, initial_losses]])
            return "Player {} successfully added!".format(name)


    def get_next_open_row(self, wks):
        i = 3
        while any(elt != '' for elt in wks.get_row(i, include_tailing_empty = False)[1:10]):
            i += 1
        return i
