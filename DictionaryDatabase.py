class DictionaryDatabase:

    def __init__(self):
        self.games = []
        self.players = {}

    def get_player_games(self, name : str):
        pass

    def get_player_data(self, player : str):
        if player not in self.players:
            return "Player {} does not exist in the database!".format(player)
        else:
            return self.players[player]

    def updatePlayerData(self, player : str, ELO : int,
        number_of_wins : int, number_of_losses : int):
        pass

    def log_game(self, timestamp : int,
            player1 : str,
            player2 : str,
            player3 : str,
            player4 : str,
            team_1_score : int,
            team_2_score : int):
        pass

    def get_leaderboard(self):
        pass



    def add_player(self, name : str, initial_elo :int, initial_wins : int, initial_losses : int):
    
        if name in self.players:
            return "Player already exists in the database!"
        else:
            self.players[name] = [initial_elo, initial_wins, initial_losses]
            return "Player {} successfully added!".format(name)
