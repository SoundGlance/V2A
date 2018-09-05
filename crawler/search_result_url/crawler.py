import sys
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote

def request(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

def crawl(search_keyword, num_collect):
    url_base = 'https://google.com/search?q=%s' % search_keyword
    url_list = []
    soup = request(url_base)
    print("Start crawling %s" % search_keyword)
    with open('result_%s.txt' % '_'.join(search_keyword.split()), 'a') as f:
        while len(url_list) < num_collect:
            for cite in soup.find_all('cite'):
                try:
                    # decodes %-escaped characters like %25
                    url = unquote(cite.parent.parent.previous_sibling.a['href'][7:])
                    # detach arguments automatically attached by Google
                    url = url[:url.find('&sa=')]
                    # add the url to the result
                    f.write("%s\n" % url)
                    url_list.append(url)
                    print("[%d] %s" % (len(url_list), url))
                except Exception as e:
                    print(e)
                    # the results in special format, such as videos, raise errors
                    continue
            # make a request of url that links to the next page of search results
            if len(url_list) < num_collect: 
                try:
                    next_url = soup.find('table', {'id': 'nav'}).find_all('td')[-1].a['href']
                    soup = request('https://google.com' + next_url)
                    time.sleep(10) # lower the query speed to prevent IP from being blocked
                except Exception as e:
                    print(e)
                    break

KEYWORDS = [
    #'태풍 대비책',
    '곤약 효과',
    #'알파고 원리',
    #'싸이 컴백',
    '아이코스 부작용',
    #'방콕 명소'
]

for keyword in KEYWORDS:
    crawl(keyword, 60)