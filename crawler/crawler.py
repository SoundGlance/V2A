import requests
import time
from bs4 import BeautifulSoup

def request(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

keyword = input()
url = 'https://google.com/search?q=%s' % keyword
soup = request(url)
print(soup)

L = []

while len(L) < 100:
    for cite in soup.find_all('cite'):
        try:
            url = cite.parent.parent.previous_sibling.a['href'][7:]
            L.append(url)
            if len(L) >= 100:
                break
        except Exception as e:
            print(e)
    next_url = soup.find('table', {'id': 'nav'}).find_all('td')[-1].a['href']
    soup = request('https://google.com' + next_url)
    print('%d/100' % len(L))
    time.sleep(5)

L = L[:100]

result = '\n'.join(['[%d] %s' % (i+1, u) for i, u in enumerate(L)])

open('result.txt', 'w').write(result)
