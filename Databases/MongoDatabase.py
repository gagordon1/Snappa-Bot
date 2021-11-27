import pymongo

class  MongoDatabase:
    def __init__(self, test = False):
        self.client = pymongo.MongoClient("mongodb+srv://garrettgordon99:Gsurfer123@snappa-database.hvg5y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        if test:
            self.gameDb = self.client.TestGameDB
            self.game = self.gameDb.TestGame

            self.playerDb = self.client.TestPlayerDB
            self.player = self.playerDb.TestPlayer
            self.clear()
        else:
            self.gameDb = self.client.GameDB
            self.game = self.gameDb.Game

            self.playerDb = self.client.PlayerDB
            self.player = self.playerDb.Player

    def clear(self):
        self.game.drop()
        self.player.drop()


    def get_player_data(self, player : str):
        players = [player for player in self.player.find({"Name" : player})]
        if players == []:
            return "Player {} does not exist in the database!".format(player)
        else:
            return [players[0]["ELO"], players[0]["Wins"], players[0]["Losses"]]

    def updatePlayerData(self, player : str, ELO : int,
        number_of_wins : int, number_of_losses : int):
        players = [player for player in self.player.find({"Name" : player})]
        if players == []:
            return "Player {} does not exist in the database!".format(player)
        else:
            query = {"Name" : player}
            newvalues = { "$set": {
                "ELO": ELO,
                "Wins": number_of_wins,
                "Losses" : number_of_losses
                }
            }
            self.player.update_one(query, newvalues)
            return "Player data successfully updated!"

    def log_game(self, timestamp : int,
            player1 : str,
            player2 : str,
            player3 : str,
            player4 : str,
            team_1_score : int,
            team_2_score : int):
        for p in [player1, player2, player3, player4]:
            players = [player for player in self.player.find({"Name" : p})]
            if players == []:
                return "Player {} does not exist in the database!".format(p)

        self.game.insert_one(
            {
                "timestamp" :  timestamp,
                "player1" :  player1,
                "player2" :  player2,
                "player3" :  player3,
                "player4" :  player4,
                "team_1_score" :  team_1_score,
                "team_2_score" :  team_2_score,
            }
        )
        return "Game successfully logged!"


    def get_leaderboard(self):
        out = []
        players = [player for player in self.player.find()]
        for player in players:
            out.append([
                player["Name"],
                player["ELO"],
                player["Wins"],
                player["Losses"]
            ])
        return out


    def get_player_games(self, name : str):
        out = []
        for i in range(1,5):
            games = [game for game in self.game.find({"player{}".format(i) : name})]
            for g in games:
                out.append([g["timestamp"], g["player1"], g["player2"], g["player3"],
                g["player4"], g["team_1_score"], g["team_2_score"]])
        return out



    def add_player(self, name : str, initial_elo :int, initial_wins : int, initial_losses : int):
        players = [player for player in self.player.find({"Name" : name})]
        if players == []:
            self.player.insert_one(
                {
                    "Name" : name,
                    "ELO" : initial_elo,
                    "Wins" : initial_wins,
                    "Losses" : initial_losses
                }
            )
            return "Player {} successfully added!".format(name)
        else: #player exists
            return "Player already exists in the database!"
