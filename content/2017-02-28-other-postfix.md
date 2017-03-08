Title: Сам себе почтальон
Date: 2017-02-28 15:00
Modified: 2017-02-28 15:00
Category: Другое
Tags: postfix, email, python, dkim, spf
Image: /media/postfix/postfix.png
Image_width: 1280
Image_height: 791
Summary:
    Каждый раз при запуске проекта в продакшн, встает вопрос, как
    отправлять письма с боевого сервера. Есть множество удобных сервисов, таких как
    [mailgun](https://www.mailgun.com/) или [mailjet](https://www.mailjet.com/),
    можно отправлять письма со своего домена через `smtp`
    [Яндекса](https://pdd.yandex.ru/). Но иногда нужно организовать свой почтовый
    сервер и рассылать письма через него.

Каждый раз при запуске проекта в продакшн, встает вопрос, как
отправлять письма с боевого сервера. Есть множество удобных сервисов, таких как
[mailgun](https://www.mailgun.com/) или [mailjet](https://www.mailjet.com/),
можно отправлять письма со своего домена через `smtp`
[Яндекса](https://pdd.yandex.ru/). Но иногда нужно организовать свой почтовый
сервер и рассылать письма через него.

На этапе разработки проекта в качестве почтового сервера мы используем
[DebugMail](https://debugmail.io) сервис, который позволяет без настройки
своего `smtp` сервера отправлять тестовые
[письма](https://debugmail.io/mails/ec14ea018ee2944ff36776c9f1ba1b186984df8a).

![Debug Mail](/media/postfix/dm.png){.center}

## Письма, письма лично на почту ношу...

Установим свой почтовый сервер, будем использовать простой и удобный
[PostFix](http://www.postfix.org/).

```bash
$ sudo apt-get install postfix
```

В интерактивном режиме указываем тип и домен нашего сервера.

![Configure Postfix](/media/postfix/ps-configure.png){.center}

![Postfix domain](/media/postfix/ps-domain.png){.center}

Для дальнейшей настройки скопируем базовый конфигурационный файл для `debian`.
И добавим доступ только из локального хоста.

```bash
$ sudo cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
$ echo "
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mydestination = localhost
" | sudo tee -a /etc/postfix/main.cf
$ sudo service postfix reload
```

По умолчанию у `postfix` открыт 25 порт из внешнего мира, закроем его,
отредактировав `etc/postfix/master.cf`.

```diff
--- /etc/postfix/master.cf
+++ /etc/postfix/master.cf
@@ -10,7 +10,7 @@
 #               (yes)   (yes)   (yes)   (never) (100)
 # ==========================================================================
 # smtp      inet  n       -       -       -       -       smtpd
-smtp               inet  n       -       n       -       -       smtpd
+127.0.0.1:smtp     inet  n       -       n       -       -       smtpd
 #smtp      inet  n       -       -       -       1       postscreen
 #smtpd     pass  -       -       -       -       -       smtpd
 #dnsblog   unix  -       -       -       -       0       dnsblog
```

Теперь можем попробовать отправить свое первое письмо с собственного сервера.
Воспользуемся для этого стандартной библиотекой `python`
[SMTPLib](https://docs.python.org/3.6/library/smtplib.html).

```python
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

text_part = MIMEText('There are test mail text content', 'plain')
html_part = MIMEText('''
<html>
  <head></head>
  <body>
    <h1>Hello from Earth<h1>
    <p>There are test mail html content.</p>
    <p style="color:red">have a good day ;)</p>
  </body>
</html>
''', 'html')

from_, to_ = 'from@some.com', 'to@other.org'

msg = MIMEMultipart('alternative')

msg['Subject'] = 'Hello from Earth'
msg['From'] = from_
msg['To'] = to_

msg.attach(text_part)
msg.attach(html_part)

host = 'localhost'
conn = smtplib.SMTP(host)
conn.sendmail(from_, [to_], msg.as_string())
conn.quit()
```

Письмо успешно отправляется и обязательно попадает в спам, т.к. выглядит
очень подозрительно и отправлено с неподтвержденного адреса.

![gmail spam](/media/postfix/gmail.png){.center .shadow}

<!-- ### Немного безопасности -->

Подключим `tls` шифрование писем, добавив следующие строки в `/etc/postfix/main.cf`

```Lighttpd
smtpd_tls_security_level = may
smtp_tls_security_level = may
smtp_tls_loglevel = 1
smtpd_tls_loglevel = 1

smtpd_tls_CAfile = /etc/letsencrypt/live/example.com/chain.pem
smtpd_tls_cert_file = /etc/letsencrypt/live/example.com/cert.pem
smtpd_tls_key_file = /etc/letsencrypt/live/example.com/privkey.pem

smtp_tls_session_cache_database = btree:/var/lib/postfix/smtp_scache

smtp_tls_mandatory_exclude_ciphers = aNULL, MD5 , DES, ADH, RC4, PSD, SRP, 3DES, eNULL
smtp_tls_mandatory_protocols = !SSLv2, !SSLv3, !TLSv1, !TLSv1.1
smtp_tls_protocols=!SSLv2, !SSLv3, !TLSv1, !TLSv1.1
smtp_tls_mandatory_ciphers=high
tls_high_cipherlist=EDH+CAMELLIA:EDH+aRSA:EECDH+aRSA+AESGCM:EECDH+aRSA+SHA384:EECDH+aRSA+SHA256:EECDH:+CAMELLIA256:+AES256:+CAMELLIA128:+AES128:+SSLv3:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!DSS:!RC4:!SEED:!ECDSA:CAMELLIA256-SHA:AES256-SHA:CAMELLIA128-SHA:AES128-SHA
tls_random_source = dev:/dev/urandom
```

Здесь нам понадобятся сертификаты, можно сгенерировать их самостоятельно,
но проще и надежнее использовать бесплатные сертификаты от [Let’s Encrypt](https://letsencrypt.org/).
Как их получить можно причтать в статье [Давайте шифровать](|filename|/2016-01-15-secure-letsencrypt.md).

После настройки перезапускаем `postfix` и проверяем доступность `tls`.

```shell
$ openssl s_client -starttls smtp -showcerts -connect localhost:25

CONNECTED(00000003)
depth=1 C = US, O = Let's Encrypt, CN = Let's Encrypt Authority X3
verify error:num=20:unable to get local issuer certificate
---
Certificate chain
 0 s:/CN=pre-loved.ru
   i:/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
-----BEGIN CERTIFICATE-----
MIIGKjCCBRKgAwIBAgISA2twWHq7oJPeB25R9BL5CR5eMA0GCSqGSIb3DQEBCwUA
MEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD
ExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xNzAyMjMxMTI1MDBaFw0x
NzA1MjQxMTI1MDBaMBcxFTATBgNVBAMTDHByZS1sb3ZlZC5ydTCCAiIwDQYJKoZI
hvcNAQEBBQADggIPADCCAgoCggIBAMPQNY69/OfkL7oV2pDtXXBiljso88X8V4DO
WqZOQ6sAhlDx4J87hF0057T0j54OA0w++9LsN64caj9oW43Hi0px6ZD32Pd7IBeU
qO7uxlC/JUwtWOcvjWo+O9qLgk50E13GwDNphkKcxD73jWUsesIbVh3YQziw9umG
NYwRlALEiJuttH7gZJYKS8P/v0XygES1zMBhINA8+akVq+PWzEaNnDqixWD2tOkq
BO+Kll2AV7fwTnpEsaLyvoOriiIvV0is7wbKVV211tzhftoHrg3Zqtet+YYKFT08
Ge77ETVb5GZqoHkFCDO6UwbwxobC3XGGG2L8vqvMhwMGUoGKwN6vZiCJgDne9Nw6
C7nd3xsWcSXvPZZoqIydEhQRAFXfGGANmTHAX91bvpnKoQFaB8V+rQxGZr65xZtR
78wOsSFpHYWbrqGBBqXVTaKUttlIkaTNp4wUgXnRZtBvMkHoZdJNqRgCTcCis9wO
/9j0UtbMuHyINrJSEnfKvgVybJV/75TTdxh42i5u4v+LTrb9RulkRAE+yU40vJCu
mH4xig7jzaGB8a2ygIG9GG4rfhAhl/UwUU7Y+CMyAVUr4If1a8h6Wza6UPhPG6xb
2TtP2sbST0kDsGsrYByO7NNgnXcGZ9We27DoPzK6IqC8y2TMDO6xe+RZhS4VhJTB
c2XF9nFbAgMBAAGjggI7MIICNzAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYI
KwYBBQUHAwEGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFDSBqGKm
lumHeQnfxldoTJIVr6ZsMB8GA1UdIwQYMBaAFKhKamMEfd265tE5t6ZFZe/zqOyh
MHAGCCsGAQUFBwEBBGQwYjAvBggrBgEFBQcwAYYjaHR0cDovL29jc3AuaW50LXgz
LmxldHNlbmNyeXB0Lm9yZy8wLwYIKwYBBQUHMAKGI2h0dHA6Ly9jZXJ0LmludC14
My5sZXRzZW5jcnlwdC5vcmcvMEUGA1UdEQQ+MDyCB3BsdmQucnWCDHByZS1sb3Zl
ZC5ydYIKcHJlbG92ZC5ydYIKcHJlbHV2ZC5ydYILcHJlbHV2ZWQucnUwgf4GA1Ud
IASB9jCB8zAIBgZngQwBAgEwgeYGCysGAQQBgt8TAQEBMIHWMCYGCCsGAQUFBwIB
FhpodHRwOi8vY3BzLmxldHNlbmNyeXB0Lm9yZzCBqwYIKwYBBQUHAgIwgZ4MgZtU
aGlzIENlcnRpZmljYXRlIG1heSBvbmx5IGJlIHJlbGllZCB1cG9uIGJ5IFJlbHlp
bmcgUGFydGllcyBhbmQgb25seSBpbiBhY2NvcmRhbmNlIHdpdGggdGhlIENlcnRp
ZmljYXRlIFBvbGljeSBmb3VuZCBhdCBodHRwczovL2xldHNlbmNyeXB0Lm9yZy9y
ZXBvc2l0b3J5LzANBgkqhkiG9w0BAQsFAAOCAQEAHGd4xQNBWZGf6c/sMDc5NIfY
YoJWonyct7vwUYcYvAFCSOPZYD+sauKGv+9Pyidbp7bfv+3xbPT6WIv4X/uRgJ5S
5n7t36HelwKHHm/6vGLZ1k2kNEM4Qd21XpHtLKNH0gNMDJnh2QIpQY7k1f6OdDa1
ZgNY366N7BcNMjy3zRbS+PdULIPYtSPq+HroO7Asw2zQ535Yx0SAwKEku4o1RyFP
Tih3dYyMUdQk0G2mUR+cN2Bx5Spa90ImxGLWk5y2+vErH4Z028aYvWeNErlUorZK
dj6f29YiiBtEhTHaIY0wDII7Mb/a8/3j3zpbxs2WpQn+oMIWQ8GZj23QLSoULQ==
-----END CERTIFICATE-----
 1 s:/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
   i:/O=Digital Signature Trust Co./CN=DST Root CA X3
-----BEGIN CERTIFICATE-----
MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/
MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT
DkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0Nlow
SjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUxldCdzIEVuY3J5cHQxIzAhBgNVBAMT
GkxldCdzIEVuY3J5cHQgQXV0aG9yaXR5IFgzMIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAnNMM8FrlLke3cl03g7NoYzDq1zUmGSXhvb418XCSL7e4S0EF
q6meNQhY7LEqxGiHC6PjdeTm86dicbp5gWAf15Gan/PQeGdxyGkOlZHP/uaZ6WA8
SMx+yk13EiSdRxta67nsHjcAHJyse6cF6s5K671B5TaYucv9bTyWaN8jKkKQDIZ0
Z8h/pZq4UmEUEz9l6YKHy9v6Dlb2honzhT+Xhq+w3Brvaw2VFn3EK6BlspkENnWA
a6xK8xuQSXgvopZPKiAlKQTGdMDQMc2PMTiVFrqoM7hD8bEfwzB/onkxEz0tNvjj
/PIzark5McWvxI0NHWQWM6r6hCm21AvA2H3DkwIDAQABo4IBfTCCAXkwEgYDVR0T
AQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8EBAMCAYYwfwYIKwYBBQUHAQEEczBxMDIG
CCsGAQUFBzABhiZodHRwOi8vaXNyZy50cnVzdGlkLm9jc3AuaWRlbnRydXN0LmNv
bTA7BggrBgEFBQcwAoYvaHR0cDovL2FwcHMuaWRlbnRydXN0LmNvbS9yb290cy9k
c3Ryb290Y2F4My5wN2MwHwYDVR0jBBgwFoAUxKexpHsscfrb4UuQdf/EFWCFiRAw
VAYDVR0gBE0wSzAIBgZngQwBAgEwPwYLKwYBBAGC3xMBAQEwMDAuBggrBgEFBQcC
ARYiaHR0cDovL2Nwcy5yb290LXgxLmxldHNlbmNyeXB0Lm9yZzA8BgNVHR8ENTAz
MDGgL6AthitodHRwOi8vY3JsLmlkZW50cnVzdC5jb20vRFNUUk9PVENBWDNDUkwu
Y3JsMB0GA1UdDgQWBBSoSmpjBH3duubRObemRWXv86jsoTANBgkqhkiG9w0BAQsF
AAOCAQEA3TPXEfNjWDjdGBX7CVW+dla5cEilaUcne8IkCJLxWh9KEik3JHRRHGJo
uM2VcGfl96S8TihRzZvoroed6ti6WqEBmtzw3Wodatg+VyOeph4EYpr/1wXKtx8/
wApIvJSwtmVi4MFU5aMqrSDE6ea73Mj2tcMyo5jMd6jmeWUHK8so/joWUoHOUgwu
X4Po1QYz+3dszkDqMp4fklxBwXRsW10KXzPMTZ+sOPAveyxindmjkW8lGy+QsRlG
PfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6
KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg==
-----END CERTIFICATE-----
---
Server certificate
subject=/CN=pre-loved.ru
issuer=/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
---
No client certificate CA names sent
Peer signing digest: SHA512
Server Temp Key: ECDH, P-256, 256 bits
---
SSL handshake has read 3884 bytes and written 468 bytes
---
New, TLSv1/SSLv3, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Server public key is 4096 bit
Secure Renegotiation IS supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: 9C05050D143CE1474438AEC0A57BD8303953053608ECD5775B565A26455EDADB
    Session-ID-ctx: 
    Master-Key: D6A09F3AC016E489542EAA11E9EFF7B56118D24F849FD480B26E219322E8D97D43DE7C537E9B928A67DDCAD3F9397EC6
    Key-Arg   : None
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - cd a5 c1 43 13 c9 2c 4b-7e 14 f6 53 92 86 89 29   ...C..,K~..S...)
    0010 - 88 dc ae cc d4 61 a1 4c-ec 05 b1 61 94 0c b1 6c   .....a.L...a...l
    0020 - 13 57 84 63 0f e4 6a d7-da 08 45 7e 80 3e fd d7   .W.c..j...E~.>..
    0030 - 16 82 70 d5 e4 8a bd ba-6f 9d b9 6f d9 49 56 b7   ..p.....o..o.IV.
    0040 - d4 41 5a c7 27 53 82 b5-8d 5d 22 08 38 3c a5 59   .AZ.'S...]".8<.Y
    0050 - 6b 06 e7 5f ba 36 2f 91-44 85 7a 5d 1c e4 da d9   k.._.6/.D.z]....
    0060 - 90 78 64 10 63 6a df c9-79 8d d9 10 66 dc 24 74   .xd.cj..y...f.$t
    0070 - fb 5a f6 f5 02 14 c5 d5-b0 b3 65 57 24 01 f2 bd   .Z........eW$...
    0080 - 06 31 f9 a9 e3 32 42 ad-f0 3b b5 3d 39 77 2c 95   .1...2B..;.=9w,.
    0090 - 8f fd e9 4f c9 4c 1d 77-8e 23 e4 ca 48 e8 9f ed   ...O.L.w.#..H...

    Start Time: 1489229346
    Timeout   : 300 (sec)
    Verify return code: 20 (unable to get local issuer certificate)
---
250 DSN
QUIT
DONE
```

<!--
Установим авториазацию с помощью [SASL](https://tools.ietf.org/html/rfc2222).

```bash
$ sudo apt-get install sasl2-bin
```

Укажим доступные пары логин\пароль в файле `/etc/postfix/sasl_passwd`.

```bash
# домен        логин:хеш пароля
example.com    testuser:59de1412ec33fd96ac4a4bfc793f1133
```

Дадим доступ на чтение этого файла только администратору и сгенерируем таблицу.

```bash
$ sudo chown root:root /etc/postfix/sasl_passwd && chmod 600 /etc/postfix/sasl_passwd
$ postmap hash:/etc/postfix/sasl_passwd
$ ls -all /etc/postfix/sasl_passwd*
-rw------- 1 root root    59 фев  28 18:31 /etc/postfix/sasl_passwd
-rw------- 1 root root 12288 фев  28 18:37 /etc/postfix/sasl_passwd.db
```

Разрешим доступ только аутентифицированным пользователям, добавив в `/etc/postfix/main.cf`

```Lighttpd
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = $myhostname
broken_sasl_auth_clients = yes
smtpd_recipient_restrictions =
   permit_sasl_authenticated, permit_mynetworks, check_relay_domains
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
```

Перезапускаем `postfix` и проверяем `SMTP` авторизацию по `telnet`.

```telnet
EHLO example.com
250-example.com
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-AUTH DIGEST-MD5 CRAM-MD5 NTLM LOGIN PLAIN
250-AUTH=DIGEST-MD5 CRAM-MD5 NTLM LOGIN PLAIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
quit
```

Следующие строки указывают на наличие аутентификации.

```telnet
250-AUTH DIGEST-MD5 CRAM-MD5 NTLM LOGIN PLAIN
250-AUTH=DIGEST-MD5 CRAM-MD5 NTLM LOGIN PLAIN
```

Проверяем отправку письма добавив авторизацию.

```python
conn = smtplib.SMTP(host)
conn.login('testuser', 'testpasswd')
```
-->
## Подписываюсь под каждым словом...

На сегодняшний день, считается обязательным подпись электронных писем
с помощью [DKIM](http://www.dkim.org/) для того чтобы почтовый сервер
получателя мог удостоверится в том, что почта отправлена именно с сервера
указанного в поле `From`.

### Установка и настройка OpenDKIM

Устанавливаем необходимые пакеты, [OpenDKIM](http://www.opendkim.org/).

```bash
$ sudo apt-get install opendkim opendkim-tools
```

Генерируем ключи и сохраняем их доступными для чтения группе `opendkim`,
а также добавляем в эту группу `postfix`.

```bash
$ sudo mkdir /etc/opendkim
$ sudo opendkim-genkey -D /etc/opendkim -d $(hostname -d) -s $(hostname)
$ sudo chgrp opendkim /etc/opendkim/*
$ sudo chmod g+r /etc/opendkim/*
$ sudo gpasswd -a postfix opendkim
```

Теперь указываем `opendkim`где находятся ключи, для этого дописываем
в конфигурационный файл `/etc/opendkim.conf` следующие строки.

```Lighttpd
Canonicalization relaxed/relaxed
SyslogSuccess yes
RequireSafeKeys false
KeyTable file:/etc/opendkim/keytable
SigningTable file:/etc/opendkim/signingtable
X-Header yes
```

Подробнее ознакомится с возможными параметрами можно в
[документации](http://www.opendkim.org/opendkim.conf.5.html).

Теперь заполним таблицы ключей в файлах `/etc/opendkim/keytable` и `/etc/opendkim/signingtable`.
Они указывают соответсвие между доменом и ключем, которым необходимо подписывать письмо.

```bash
# /etc/opendkim/keytable
ключ домен:селектор:/путь/до/ключа
```

```bash
# /etc/opendkim/signingtable
домен ключ
```

Например:

```bash
# /etc/opendkim/keytable
mail._domainkey.example.com example.com:mail:/etc/opendkim/mail.private
```

```bash
# /etc/opendkim/signingtable
example.com    mail._domainkey.example.com
```

### Настройка Postfix для работы с OpenDKIM

Указываем о необходимости подписывать все письма с помощью `dkim`.

```bash
$ sudo postconf -e milter_default_action=accept
$ sudo postconf -e milter_protocol=2
$ sudo postconf -e smtpd_milters=unix:/var/run/opendkim/opendkim.sock
$ sudo postconf -e non_smtpd_milters=unix:/var/run/opendkim/opendkim.sock
```

Перезапускаем службы и отправляем подписанное письмо.

```bash
$ sudo service postfix restart
$ sudo service opendkim restart
```

## Настроийки доменной зоны

Чтобы сервер мог удостовериться в корректности подписи,
нужно добавить `TXT` запись содежащую ключ. Сделать это нужно в контрольной
панели регистратора. Проверим, что `dns` зоны обновились.

```bash
$ dig +short TXT mail._domainkey.example.com
"v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCvfTJ37Gqs06fhG0YYj/6HbojCrDp
F8X6u20YUaOax+jrvO0KtItfWYUi6hkCJeKbGTAOmqhWLu1T/DMt0XaICAJ7Q8525Z4ghwfvc5LgYyNSDEODeF
LNPlXgn3IP5o6Og2We/SnO4QCv8drKGf0N2xm5IIzIT8CjsbM6gPQIHTQIDAQAB"
```

Также хорошо указать разрешенные `ip` адреса для исходящих писем в запись `spf`.

```bash
$ dig +short TXT example.com
"v=spf1 a:example.com ip4:<ip v4 addr> ip6:<ip v6 addr> ~all"
```

## Все не как у людей

Сегодня мы живем в далеком и почти светлом будущем, когда по бескрайним
просторам сети широко распространяется `ipv6` адресация. Но, оказывается,
абсолютно все письма отправленные с `ipv6` всегда воспринимаются гуглом как спам.
Даже пройдя верефикацию по `dkim` и `spf` записям, уходят в нежелательную почту.

Так что укажем в конфигурации `postfix` отправку только с использованием `ipv4`.

```bash
$ sudo postconf -e inet_protocols=ipv4
```

Теперь письма успешно доставляются и проходят все валидации.

![gmail ok](/media/postfix/gmail_ok.png){.center .shadow}

<details>
    <summary>Пример письма</summary>
```python
Delivered-To: samael500@gmail.com
Received: by 10.182.174.67 with SMTP id bq3csp1452226obc;
        Tue, 28 Feb 2017 08:09:52 -0800 (PST)
X-Received: by 10.46.22.18 with SMTP id w18mr1151641ljd.86.1488298192253;
        Tue, 28 Feb 2017 08:09:52 -0800 (PST)
Return-Path: <info@*********>
Received: from ********* (*********. [**.**.**.**])
        by mx.google.com with ESMTPS id x14si1225569lfd.155.2017.02.28.08.09.51
        for <samael500@gmail.com>
        (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);
        Tue, 28 Feb 2017 08:09:52 -0800 (PST)
Received-SPF: pass (google.com: domain of info@********* designates **.**.**.** as permitted sender) client-ip=**.**.**.**;
Authentication-Results: mx.google.com;
       dkim=pass header.i=*********;
       spf=pass (google.com: domain of info@********* designates **.**.**.** as permitted sender) smtp.mailfrom=info@*********
Received: from ********* (localhost [127.0.0.1])
    by ********* (Postfix) with ESMTP id D9ED0452AB
    for <samael500@gmail.com>; Tue, 28 Feb 2017 16:09:53 +0000 (UTC)
DKIM-Filter: OpenDKIM Filter v2.9.2 ********* D9ED0452AB
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=*********;
    s=mail; t=1488298193;
    bh=juRoCRHzIAJJ4fKO8VlXEyxNddxTS8ftBnWmLxjdAik=;
    h=Subject:From:To:Date:From;
    b=G0Z6uXOV0LQHscdUOwMg5rjuJA/KWZ7x6Iqx3Z2x01nZ2kD+E1OgyP4zEfqS9XDiS
     fG04P0qpIJyGEmO8hgRDIlH1d5FIDGjGPMAFDynwZ9j7pG1h88yLHThdtesUN7Fjib
     2yL1xxiyw2dZbtfvgXwhj0Nb9RXpphrY+c9v2fW4=
Content-Type: multipart/alternative;
 boundary="===============3211535685628593130=="
MIME-Version: 1.0
Subject: Hello from Earth
From: info@*********
To: samael500@gmail.com
Message-Id: <20170228160953.D9ED0452AB*********>
Date: Tue, 28 Feb 2017 16:09:53 +0000 (UTC)

--===============3211535685628593130==
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

There are test mail text content
--===============3211535685628593130==
Content-Type: text/html; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit


<html>
  <head></head>
  <body>
    <h1>Hello from Earth<h1>
    <p>There are test mail html content.</p>
    <p style="color:red">have a good day ;)</p>
  </body>
</html>

--===============3211535685628593130==--
```
</details>


## Django settings

Теперь можно подключить отправку писем через наш `smtp` в джанго.

```python
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'info@example.com'
```
