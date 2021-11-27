"""
PARSE STRUCTURE

add player
@SnappaBot add @<name>

log score
@SnappaBot @<name> @<name> @<name> @<name> <score_1> <score_2>

get leaderboard
@SnappBot lb

get player data
@SnappaBot @<name>

none

"""

def parse_text(text):
    """Parses a new message in the groupme

    Parameters
    ----------
    text : str
        Incoming message text

    Returns
    -------
    tuple
        "Not invoking SnappaBot!" |
        "Improper formatting!"    |
        (action, list(string))

        tuple containing a string saying the action in the first index
        and list of parameters in the second index
    """
