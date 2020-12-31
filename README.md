# ichigekisan
- サイトで配布されているアプリケーションのバージョン
- FTPサーバー上に置いているアプリケーションのバージョン(txtファイルのファイル名)

を比較し、メールで通知する。

## .env例
```
API_URL=http://example.com/brynhildr/api/

FTP_HOST=192.168.1.*
FTP_PORT=22
FTP_USER=username
FTP_PASS=password
PRIVATE_KEY_FILE_PATH=${USERPROFILE}\.ssh\id_rsa
TARGET_DIRECTORY=/share

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=example@gmail.com
SMTP_PASS=password
MAIL_TO=sendto@gmail.com
```

### FTPの認証について
PRIVATE_KEY_FILE_PATHが空の場合(`PRIVATE_KEY_FILE_PATH=`)  
FTP_PASSで認証を行う。

### PRIVATE_KEY_FILE_PATH例
- Windowsの場合 
  PRIVATE_KEY_FILE_PATH=${USERPROFILE}\.ssh\id_rsa
  
- Windows以外の場合
  PRIVATE_KEY_FILE_PATH=${HOME}/.ssh/id_rsa

たぶん上記のように「${USERPROFILE} or ${HOME}」とセパレータを変える必要あり。
Macでは未確認。

## FTPサーバー
ファイル置き場は任意の場所でOK。
.env例では`TARGET_DIRECTORY`が`/share`なので、下記の構成にしておく。

share  
　└─ brynhildr  
　　　├── *.*.*.txt  
　　　├── brynhildr.dll  
　　　└── brynhildr.exe  

txtファイルは空でいいので、ファイル名をバージョン表記にしておく。

## cryptographyインストール
paramikoインストール時にインストールされるcryptographyのインストールに失敗することあり。
以下を実行してからインストールする。
`sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`

参考：
https://cryptography.io/en/latest/installation.html
