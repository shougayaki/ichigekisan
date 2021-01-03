import sys
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


class Mail:
    def __init__(self, smtp_dict):
        self.smtp_dict = smtp_dict.copy()

    def create_message(self, body_dict):
        msg = MIMEText(body_dict['body'])
        msg['Subject'] = body_dict['subject']
        msg['To'] = self.smtp_dict['mail_to']
        msg['Date'] = formatdate()
        return msg

    def send_mail(self, msg):
        smtp_obj = smtplib.SMTP(self.smtp_dict['smtp_server'], self.smtp_dict['smtp_port'])
        try:
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.login(self.smtp_dict['smtp_user'], self.smtp_dict['smtp_pass'])
            smtp_obj.sendmail(self.smtp_dict['smtp_user'], self.smtp_dict['mail_to'], str(msg))
            return {'result': True, 'msg': 'Mail Send Succeeded'}
        except Exception as e:
            # エラー内容、エラーが発生したファイル、エラーが発生した行数を取得
            exc_type, _, exc_tb = sys.exc_info()
            file_name = Path(exc_tb.tb_frame.f_code.co_filename).name
            return {'result': False, 'msg': '{}<{}><{}: line {}>'.format(exc_type, e, file_name, exc_tb.tb_lineno)}
        finally:
            smtp_obj.close()
