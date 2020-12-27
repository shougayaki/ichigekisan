import os
from dotenv import load_dotenv
from pathlib import Path


def config():
    dotenv_path = Path(__file__).resolve().parents[1].joinpath('.env')
    load_dotenv(dotenv_path)
    conf = {
        'url_info': {
            'url': os.environ.get('URL'),
            'app_name': os.environ.get('APP_NAME'),
            'download_url': os.environ.get('DOWNLOAD_URL')
        },
        'ftp_info': {
            'ftp_uri': os.environ.get('FTP_URI'),
            'ftp_user': os.environ.get('FTP_USER'),
            'ftp_pass': os.environ.get('FTP_PASS')
        },
        'mail_info': {
            'smtp_server': os.environ.get('SMTP_SERVER'),
            'smtp_port': os.environ.get('SMTP_PORT'),
            'smtp_user': os.environ.get('SMTP_USER'),
            'smtp_pass': os.environ.get('SMTP_PASS'),
            'mail_to': os.environ.get('MAIL_TO')
        }
    }
    return conf
