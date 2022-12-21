import requests


url = 'https://akabab.github.io/superhero-api/api'
urn = '/all.json'
hero_list = ['Hulk', 'Captain America', 'Thanos']

response = [hero for hero in requests.get(url + urn).json() if hero['name'] in hero_list]

max_intelligence = max(hero['powerstats']['intelligence'] for hero in response)

res = [hero['name'] for hero in response if hero['powerstats']['intelligence'] == max_intelligence]

print(res[0])