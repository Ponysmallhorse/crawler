from bs4 import BeautifulSoup

def get_text(data):
    soup = BeautifulSoup(data, "html5lib")
    for elem in soup.find_all(['script', 'style']):
        elem.extract()
    return soup.getText()

def get_links(data, home = None):
    soup = BeautifulSoup(data, "html5lib")
    return [a.attrs.get('href') if a.attrs.get('href') is not None \
                                   and (a.attrs.get('href').startswith('http') or  a.attrs.get('href').startswith('www')) \
                else None for a in soup.select('a')]


if __name__ == "__main__":
    import urllib3
    import os

    http_pool = urllib3.PoolManager()
    req = http_pool.request('GET', 'https://www.nytimes.com')

    with open(os.path.join(os.path.dirname(__file__), 'nytimes2.txt'), 'w+') as f:
        f.write(str(get_links(req.data)))
