import requests


def send_to_groupme(base_url, bot_id, text):
    """Posts a message to the groupme

    Parameters
    ----------
    base_url : str
        groupme post message url endpoint
    bot_id : int
        Id of the bot
    text : str
        text of message to send

    Returns
    -------
    str
        groupme response | "Failed to post message!"

    """
    data = {
        "bot_id" : bot_id,
        "text" : text
    }
    try:
        requests.post(base_url, json = data)
        response = "Successfully sent {} in the groupme".format(message)
    except:
        response = "Failed to post message!"
    return response

if __name__ == '__main__':
    BOT_ID = "d9ce63918a5ba0a22008fa71dc"
    BASE_URL = "https://api.groupme.com/v3/bots/post"
    message = "Hello"
    send_to_groupme(BASE_URL, BOT_ID, message)
