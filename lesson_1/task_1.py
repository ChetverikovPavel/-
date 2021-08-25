import requests
import json


response = requests.get('https://api.github.com/users/ChetverikovPavel/repos')

print(response)

if response.ok:
    j_data = response.json()
    with open('data.json', 'w') as f:
        json.dump(j_data, f)
        for repo in j_data:
            print(repo.get('full_name'))





