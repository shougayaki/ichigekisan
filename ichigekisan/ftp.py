import ftplib


class ConnectFtp:
    def __init__(self, ftp_dict, app_name):
        self.ftp_dict = ftp_dict.copy()
        self.app_name = app_name

    def ftp_file_list(self):
        try:
            ftp = ftplib.FTP_TLS(
                self.ftp_dict['ftp_uri'],
                self.ftp_dict['ftp_user'],
                self.ftp_dict['ftp_pass']
            )
            ftp.prot_p()
            if self.app_name in ftp.nlst('.'):
                ftp.cwd(self.app_name)
                files = ftp.nlst('.')
            else:
                files = 'Not found [{}] directory on server.'.format(self.app_name)
        except ftplib.all_errors as e:
            return str(e)
        else:
            ftp.quit()

        return files
