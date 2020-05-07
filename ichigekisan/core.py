import os
from config import config
from ftp import ConnectFtp
from scraping import Scraping
from mail import Mail
from distutils.version import StrictVersion
import re


def current_version(ftp_dict, app_name):
    con = ConnectFtp(ftp_dict, app_name)
    file_list = con.ftp_file_list()
    # リストで取得できたら
    if isinstance(file_list, list):
        # [ver].txtファイルをバージョン表記ソートして、最大値(配列最後)を抜き出し
        pattern = re.compile('[0-9].[0-9].[0-9].txt')
        ver_list = sorted([ver.replace('.txt', '') for ver in file_list if re.match(pattern, ver)], key=StrictVersion)
        # バージョン取得できたら
        current = ver_list[-1] if len(ver_list) > 0 else 'Version file is NOT found on server.'

        return current
    else:
        return file_list


def latest_version(url):
    scp = Scraping(url)
    ver_dict = scp.fetch_version()
    return ver_dict


def create_body(ver_current, latest, app_name):
    # 最新版はdictかステータスコードで返ってくる
    ver_latest = latest['version'] if isinstance(latest, dict) else latest

    body = (f'Current Version : {ver_current}\n'
            f'Latest Version  : {ver_latest}\n\n')

    # バージョンに差異があればダウンロードリンク表示
    body += 'DownloadLink:{}'.format(latest['download_link']) if ver_current < ver_latest else ''

    body_dict = {
        'subject': '{} Version Info'.format(app_name),
        'body': body
    }
    return body_dict


def main():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    cfg = config(current_dir)
    # バージョン確認するアプリ名
    app_name = cfg['url_info']['app_name']

    # FTP接続してバージョン取得
    current = current_version(cfg['ftp_info'], app_name)
    # サイトからバージョン取得
    latest = latest_version(cfg['url_info'])

    # メール送信
    body = create_body(current, latest, app_name)
    mailer = Mail(cfg['mail_info'])
    msg = mailer.create_message(body)
    mailer.send_mail(msg)


if __name__ == '__main__':
    main()
