import paramiko


class Ftp:
    def __init__(self, ftp_dict, app_name):
        self.ftp_dict = ftp_dict.copy()
        self.app_name = app_name

    def file_list(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        try:
            # 秘密鍵が空ならパスワードを使用する
            if self.ftp_dict['private_key_file_path'] == '':
                ssh.connect(
                    self.ftp_dict['ftp_host'],
                    self.ftp_dict['ftp_port'],
                    username=self.ftp_dict['ftp_user'],
                    password=self.ftp_dict['ftp_pass'],
                )
            else:
                rsa_key = paramiko.RSAKey.from_private_key_file(self.ftp_dict['private_key_file_path'])
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    self.ftp_dict['ftp_host'],
                    self.ftp_dict['ftp_port'],
                    username=self.ftp_dict['ftp_user'],
                    pkey=rsa_key
                )

            sftp = ssh.open_sftp()
            sftp.chdir(self.ftp_dict['target_directory'])
            if self.app_name in sftp.listdir():
                sftp.chdir(self.app_name)
                return sftp.listdir()
            else:
                return 'Not found [{}] directory on server.'.format(self.app_name)
        except Exception as e:
            return str(e)
        finally:
            ssh.close()
