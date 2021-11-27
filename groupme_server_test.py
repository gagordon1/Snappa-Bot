
import requests
API_URL = "http://localhost:5000"
#FAKE GROUPME REQUEST



def send_groupme_request(text, name):
    data = {
        "text" : text,
        "name" : name
    }
    response = requests.post("http://localhost:5000", json = data)

if __name__ == '__main__':

    # names = ["Garrett Gordon", "Andrei Dumitrescu", "Noah Faro", "Sebastian Simon"]
    # for name in names:
    #     text = "@SnappaBot /add @{}".format(name)
    #     send_groupme_request(text, name)

    # text = "@SnappaBot /score @{} @{} @{} @{}, 7-2".format(*names)
    # text = "@SnappaBot /lb"
    text = "@SnappaBot fuck u"
    send_groupme_request(text, "Garrett Gordon")
