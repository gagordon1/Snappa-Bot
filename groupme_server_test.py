import requests

BASE_URL = "http://127.0.0.1:5000"


data = {
  "attachments": [],
  "avatar_url": "https://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id": "1234567890",
  "id": "1234567890",
  "name": "John",
  "sender_id": "12345",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": False,
  "text": "Hello world ",
  "user_id": "1234567890"
}
response = requests.post(BASE_URL, data = data)
print(response.text)
