
from SnappaLeaderboard import SnappaLeaderboard, generate_leaderboard_string


def addPlayerTest1():
    """Add a player and verify that the leaderboard was updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
    leaderboard = SnappaLeaderboard()
    name = "Garrett"
    leaderboard.add_player(name)
    lb = leaderboard.get_leaderboard()
    assert lb == "SNAPPA LEADERBOARD"


def logScoreTest1():
    """Add a score and verify that the leaderboard was updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """

def getPlayerHistoryTest1():
    """Adds players, log some games then verifies a correct player
    history

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise


    """
