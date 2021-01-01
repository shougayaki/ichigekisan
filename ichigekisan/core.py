import re
from pathlib import Path
from config import config
from logger import Logger
from distutils.version import StrictVersion
from ftp import Ftp
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


def create_mail_content(**kwargs):
    body = ('Current Version : {}\n'
            'Latest Version  : {}').format(kwargs['ver_current'], kwargs['ver_latest'])

    # バージョンに差異があればダウンロードリンク表示
    if kwargs['is_updated']:
        body += '\n\nDownloadLink:{}'.format(kwargs['download_link'])

    mail_content = {
        'subject': '{} Version Info'.format(kwargs['app_name']),
        'body': body
    }
    return mail_content


def main():
    root_dir = Path(__file__).resolve().parents[1]
    cfg = config()
    log = Logger(root_dir, 10)
    info = AppInfo(cfg['api_url'])
    log.logging('=== {} Started ==='.format(root_dir.name))

    # APIからアプリ情報取得
    app_info = info.fetch_app_info()
    if isinstance(app_info, dict):
        # アプリ情報取得できたら現在のバージョン取得
        ver_current = app_info['current_version']
        log.logging('Result to fetch current version: {}'.format(ver_current))

        # サイトからバージョン取得
        latest = info.fetch_latest_version(app_info)
        ver_latest = latest['version'] if latest['download_link'] is not None else 'FAILED to fetch latest version.'
        log.logging('Result to fetch latest version: {}'.format(ver_latest))

        is_updated = False
        try:
            is_updated = StrictVersion(ver_current) < StrictVersion(ver_latest)
        except ValueError:
            pass

        # メール送信
        mail_parts = {
            'app_name': app_info['name'],
            'ver_current': ver_current,
            'ver_latest': ver_latest,
            'download_link': latest['download_link'],
            'is_updated': is_updated
        }
        mail_content = create_mail_content(**mail_parts)
        mailer = Mail(cfg['mail_info'])
        msg = mailer.create_message(mail_content)
        mail_result = mailer.send_mail(msg)
        log.logging('Result to send mail: {}'.format(mail_result))
    else:
        log.logging('FAILED to fetch app info from [{}]'.format(cfg['api_url']))
        log.logging('Error: {}'.format(app_info))

    log.logging('=== {} Stop ==='.format(root_dir.name))


if __name__ == '__main__':
    main()
