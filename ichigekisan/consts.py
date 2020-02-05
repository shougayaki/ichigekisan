import os
from dotenv import load_dotenv
import pathlib


dotenv_path = pathlib.Path(__file__).joinpath('../..', '.env')
load_dotenv(dotenv_path.resolve())

URL_INFO = {
    'url': 'http://blog.x-row.net/?p=2455#download',
    'app_name': 'brynhildr',
    'download_url': 'http://blog.x-row.net/download/?file=brynhildr&ver=',
    'connect_to': 30,
    'read_to': 60
}

FTP_INFO = {
    'ftp_uri': os.environ.get('FTP_URI'),
    'ftp_user': os.environ.get('FTP_USER'),
    'ftp_pass': os.environ.get('FTP_PASS')
}

MAIL_INFO = {
    'smtp_server': os.environ.get('SMTP_SERVER'),
    'smtp_port': os.environ.get('SMTP_PORT'),
    'smtp_user': os.environ.get('SMTP_USER'),
    'smtp_pass': os.environ.get('SMTP_PASS'),
    'mail_to': os.environ.get('MAIL_TO')
}
