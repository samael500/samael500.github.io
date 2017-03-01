Title: Сам себе почтальон
Date: 2017-02-28 15:00
Modified: 2017-02-28 15:00
Category: Другое
Tags: postfix, email, python, dkim, spf
Image: /media/wbt3/3year.png
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
