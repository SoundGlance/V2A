import sys
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote

def request(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def crawl(search_keyword):
    url = 'https://google.com/search?q=%s' % search_keyword
    soup = request(url)

    url_list = [] # crawled url's are collected in this list

    num_collect = int(sys.argv[1]) if len(sys.argv) > 1 else 100 # the number of url's to collect

    while len(url_list) < num_collect:
        for cite in soup.find_all('cite'):
            try:
                # decodes %-escaped characters like %25
                url = unquote(cite.parent.parent.previous_sibling.a['href'][7:])
                # detach arguments automatically attached by Google
                url = url[:url.find('&sa=')]
                # add the url to the result
                url_list.append(url)
                if len(url_list) >= num_collect:
                    break
            except Exception as e:
                print(e)
                # the results in special format, such as videos, raise errors
                continue
        # make a request of url that links to the next page of search results
        try:
            next_url = soup.find('table', {'id': 'nav'}).find_all('td')[-1].a['href']
            soup = request('https://google.com' + next_url)
            print('%s %d/%d' % (search_keyword, len(url_list), num_collect))
            time.sleep(5) # lower the query speed to prevent IP from being blocked
        except Exception as e:
            print(e)
            break

    result = '\n'.join(['[%d] %s' % (i, u) for i, u in enumerate(url_list)])

    open('result_%s.txt' % '_'.join(search_keyword.split()), 'w').write(result)


for keyword in ['가상화폐 원리', '방탄소년단 컴백', '전자담배 부작용', '다낭 명소', '미세먼지 대비책', '살충제 계란 유해성']:
    crawl(keyword)
