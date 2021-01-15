import os
from dotenv import load_dotenv
from pathlib import Path


def config():
    dotenv_path = Path(__file__).resolve().parents[1].joinpath('.env')
    load_dotenv(dotenv_path)
    conf = {
        'api_url': os.environ.get('API_URL'),
        'mail_info': {
            'smtp_server': os.environ.get('SMTP_SERVER'),
            'smtp_port': os.environ.get('SMTP_PORT'),
            'smtp_user': os.environ.get('SMTP_USER'),
            'smtp_pass': os.environ.get('SMTP_PASS'),
            'mail_to': os.environ.get('MAIL_TO')
        }
    }
    return conf
