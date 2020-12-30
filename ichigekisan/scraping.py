import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self, url_dict):
        self.url_dict = url_dict.copy()
        self.ua = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                   'AppleWebKit/537.36 (KHTML, like Gecko)'
                   'Chrome/87.0.4280.88 Safari/537.36')

    def fetch_version(self):
        ver_dict = {}
        try:
            res = requests.get(self.url_dict['url'], headers={'User-Agent': self.ua}, timeout=(3, 6))
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'html.parser')
                download_url = self.url_dict['download_url']

                # aタグでリンクにDownloadURLを含んでいたらバージョンとDownloadURLをdictにして返す
                for a in soup.find_all('a'):
                    if 'href' in a.attrs and download_url in a.get('href'):
                        ver_dict['version'] = a.string
                        ver_dict['download_link'] = a.get('href')
                        return ver_dict
            else:
                ver_dict['version'] = 'Status Code: {}'.format(res.status_code)
                ver_dict['download_link'] = None
        except Exception as e:
            ver_dict['version'] = 'Error: {}'.format(e)
            ver_dict['download_link'] = None
        else:
            res.close()

        return ver_dict
