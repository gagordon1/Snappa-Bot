"""
PARSE STRUCTURE

add player
@SnappaBot /add @<name>

log score
@SnappaBot /score @<name> @<name> @<name> @<name>, <score_1> <score_2>

get leaderboard
@SnappBot /lb

get player data
@SnappaBot @<name>

error

none

"""

BOT_NAME = "SnappaBot"

def parse_text(text : str, n : int):
    """Parses a new message in the groupme

    Parameters
    ----------
    text : str
        Incoming message text
    n : int
        Number of leaderboard entries to return

    Returns
    -------
    tuple
        (action, list(string))

        tuple containing a string saying the action in the first index
        and list of parameters in the second index
    """
    bot_handle = "@" + BOT_NAME
    try:
        if len(text) >= len(bot_handle) and text[:len(bot_handle)] == bot_handle:
            #addressing snappa bot
            remaining = text[len(bot_handle):]
            if "/add" in remaining:
                name = remaining[5:].strip(" @")
                return "add player", name.strip()
            elif "/lb" in remaining:
                return "get leaderboard", [n]
            elif "/score" in remaining:
                data = remaining[7:].strip().split(",")
                names = [name.strip() for name in data[0].strip("@").split("@")]
                score = [int(x) for x in data[1].strip().split("-")]
                return "log score", names + score

            elif "@" in remaining:
                name = remaining[1:].strip("@ ")
                return "get player data", name.strip()
    except:
        return "error", []

    return "none", []

if __name__ == '__main__':
    for message in [
        "@SnappaBot /add @Garrett Gordon",
        "@SnappaBot /score @Garrett Gordon @Andrei @Sebastian @Noah, 7-3",
        "@SnappaBot /lb",
        "@SnappaBot @Garrett Gordon"
    ]:
        print("\n" + "---"*10)
        print("Parsing:", message)
        action, parameters = parse_text(message, 10)

        print(action)
        print(parameters)
