import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self, url_dict):
        self.url_dict = url_dict.copy()

    def fetch_version(self):
        res = requests.get(self.url_dict['url'], timeout=(self.url_dict['connect_to'], self.url_dict['connect_to']))

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            download_url = self.url_dict['download_url']

            # aタグでリンクにDownloadURLを含んでいたらバージョンとDownloadURLをdictにして返す
            for a in soup.find_all('a'):
                if 'href' in a.attrs and download_url in a.get('href'):
                    ver_dict = {
                        'version': a.string,
                        'download_link': a.get('href')
                    }
                    return ver_dict
        else:
            version = res.status_code
        res.close()

        return version
