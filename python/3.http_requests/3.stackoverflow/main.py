from datetime import datetime
from datetime import date
import html
import requests

today = int(datetime.now().timestamp())

url = 'https://api.stackexchange.com/'
urn = '/2.3/questions'
params = {'site': 'stackoverflow',
          'tagged': 'python',
          'pagesize': 100,
          'page': 1,
          'fromdate': today - 2 * 24 * 60 * 60,
          'todate': today}
items = []
has_more = True
while has_more:
    print('.', end='')
    response = requests.get(url + urn, params=params).json()
    items += [question.get('title') for question in response.get('items')]
    params['page'] += 1
    has_more = response.get('has_more')

print()
for item in items:
    print(html.unescape(item))
print()
print(f'Всего запросов за два дня (c {date.fromtimestamp(today - 2 * 24 * 60 * 60)} '
      f'по {date.fromtimestamp(today)}): {len(items)}')

