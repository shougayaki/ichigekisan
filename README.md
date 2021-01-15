# ichigekisan
- サイトで配布されているアプリケーションのバージョン
- 自身で用意したAPIから取ってきたアプリケーションのバージョン

を比較し、メールで通知する。

## .env例
```
API_URL=http://example.com/brynhildr/api/

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=example@gmail.com
SMTP_PASS=password
MAIL_TO=sendto@gmail.com
```

## API
適当なところに以下のようなファイルを置いておいて、[.env](##.env例)のAPI_URLから引っ張ってくる。  
current_version箇所はメンテが必要。

```php:index.php
<?php
$array = [
    'name' => 'brynhildr',
    'url' => 'http://blog.x-row.net/?p=2455',
    'current_version' => '2.6.0',
    'download_url' => 'http://blog.x-row.net/download/?file=brynhildr&ver='
];
header("Content-Type: application/json; charset=utf-8");
echo json_encode($array);
```

## cryptographyインストール
paramikoインストール時にインストールされるcryptographyのインストールに失敗することあり。
以下を実行してからインストールする。
`sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`

参考：
https://cryptography.io/en/latest/installation.html
