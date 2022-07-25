import requests
import json
app_id = "fb36d843"
app_key = "8c294d37ffe76be5c44789492253a90c"
language = "en-gb"
word_id = "example"
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
r = requests.get(url, headers={"app_id": app_id, "app_key": app_key}) 
print(json.dumps(r.json()))
