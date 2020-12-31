import re
from pathlib import Path
from config import config
from logger import Logger
from distutils.version import StrictVersion
from ftp import ConnectFtp
from app_info import AppInfo
from mail import Mail


def current_version(ftp):
    ftp_res = ftp.file_list()
    # リストで取得できたら
    if isinstance(ftp_res, list):
        # [ver].txtファイルをバージョン表記ソートして、最大値(配列最後)を抜き出し
        pattern = re.compile('[0-9].[0-9].[0-9].txt')
        ver_list = sorted([ver.replace('.txt', '') for ver in ftp_res if re.match(pattern, ver)], key=StrictVersion)
        # バージョン取得できたら
        current = ver_list[-1] if len(ver_list) > 0 else 'Version file is NOT found on server.'
        return current
    else:
        return ftp_res


def create_body(ver_current, latest, app_name):
    # 最新版はdictで返ってくる。バージョン取れなかったらversionのvalueはNoneで返ってくる。
    ver_latest = latest['version'] if 'version' in latest else 'FAILED to fetch latest version.'
    body = (f'Current Version : {ver_current}\n'
            f'Latest Version  : {ver_latest}')

    # バージョン比較
    is_updated = False
    try:
        is_updated = StrictVersion(ver_current) < StrictVersion(ver_latest)
    except ValueError:
        pass

    # バージョンに差異があればダウンロードリンク表示
    if (latest['download_link'] is not None) and is_updated:
        body += '\n\nDownloadLink:{}'.format(latest['download_link'])

    body_dict = {
        'subject': '{} Version Info'.format(app_name),
        'body': body
    }
    return body_dict


def main():
    root_dir = Path(__file__).resolve().parents[1]
    cfg = config()
    log = Logger(root_dir, 10)
    version = AppInfo(cfg['api_url'])
    log.logging('=== {} Started ==='.format(root_dir.name))

    # APIからアプリ情報取得
    app_info = version.fetch_app_info()
    if isinstance(app_info, dict):
        # アプリ情報取得できたら名前と現在のバージョン取得
        app_name = app_info['name']
        ver_current = app_info['current_version']
        log.logging('Result to fetch current version: {}'.format(ver_current))

        # サイトからバージョン取得
        ver_latest = version.fetch_latest_version(app_info)
        log.logging('Result to fetch latest version: {}'.format(ver_latest['version']))

        # メール送信
        body = create_body(ver_current, ver_latest, app_name)
        mailer = Mail(cfg['mail_info'])
        msg = mailer.create_message(body)
        mail_result = mailer.send_mail(msg)
        log.logging('Result to send mail: {}'.format(mail_result))
    else:
        log.logging('FAILED to fetch app info from [{}].'.format(cfg['api_url']))

    log.logging('=== {} Stop ==='.format(root_dir.name))


if __name__ == '__main__':
    main()
