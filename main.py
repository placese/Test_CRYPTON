import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.google.com/search?q=scrapy'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
           'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(text):
    soup = BeautifulSoup(text, 'html.parser')
    items = soup.find_all('div', class_='g')
    items.pop()
    result = []

    for item in items:
        Name = item.find('h3', class_='LC20lb DKV0Md').text
        Url = item.find('a').get('href')
        Description = item.find('div', class_='IsZvec').text
        result.append({
            'Name': Name,
            'Url': Url,
            'Description': Description
        })

    return result


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        result = get_content(html.text)
        # print(json.dumps(result, ensure_ascii=False))
        with open('data.json', 'w', encoding='UTF-8') as file:
            json.dump(result, file, ensure_ascii=False)
    else:
        raise Exception("Error")


if __name__ == '__main__':
    parse()
