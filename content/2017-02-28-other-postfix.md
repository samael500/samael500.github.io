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
    сервер и разсылать письма через него.

Каждый раз при запуске проекта в продакшн, встает вопрос, как
отправлять письма с боевого сервера. Есть множество удобных сервисов, таких как
[mailgun](https://www.mailgun.com/) или [mailjet](https://www.mailjet.com/),
можно отправлять письма со своего домена через `smtp`
[Яндекса](https://pdd.yandex.ru/). Но иногда нужно организовать свой почтовый
сервер и разсылать письма через него.

На этапе разработки проекта, в качестве почтового сервера, мы используем
[DebugMail](https://debugmail.io), сервис который позволяет без настройки
своего `smtp` сервера отправлять тестовые
[письма](https://debugmail.io/mails/ec14ea018ee2944ff36776c9f1ba1b186984df8a).

![Debug Mail](/media/postfix/dm.png){.center}

## Письма письма лично на почту ношу...

Установим свой почтовый сервер, будем использовать простой и удобный
[PostFix](http://www.postfix.org/).

```shell
$ sudo apt-get install postfix
```

В интерактивном режиме указываем, тип и домен нашего сервера.

![Configure Postfix](/media/postfix/ps-configure.png){.center}

![Postfix domain](/media/postfix/ps-domain.png){.center}

Для дальнейшей настройки, скопируем базовый конфигурационный файл для `debian`.
И добавим доступ только из локального хоста.

```shell
$ sudo cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
$ echo "
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mydestination = localhost
" | sudo tee -a /etc/postfix/main.cf
$ sudo service postfix reload
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

Письмо успешно отправляется, и обязательно попадает в спам, т.к. выглядит
очень подозрительно, и отправлено с неподтвержденного адреса.

![gmail spam](/media/postfix/gmail.png){.center .shadow}

Подключим `tls` шифрование писем добавив следующие строки в `/etc/postfix/main.cf`

```
smtpd_tls_security_level = may
smtp_tls_security_level = may
smtp_tls_loglevel = 1
smtpd_tls_loglevel = 1
```

## Подписываюсь под каждым словом...

На сегодняшний день, считается обязательным подпись электронных писем
с помощью [DKIM](http://www.dkim.org/), для того что бы почтовый сервер
получателя мог удостоверится в том, что почта отправлена именно с сервера
указанного в поле `From`.

### Установка и настройка OpenDKIM

Устанавливаем необходимые пакеты, [OpenDKIM](http://www.opendkim.org/).

```shell
$ sudo apt-get install opendkim opendkim-tools
```

Генерируем ключи и сохраняем их доступными для чтения группе `opendkim`,
а так же добавляем в эту группу `postfix`. 

```shell
$ sudo mkdir /etc/opendkim
$ sudo opendkim-genkey -D /etc/opendkim -d $(hostname -d) -s $(hostname)
$ sudo chgrp opendkim /etc/opendkim/*
$ sudo chmod g+r /etc/opendkim/*
$ sudo gpasswd -a postfix opendkim
```

Теперь указываем `opendkim` где находятся ключи, для этого дописываем
в конфигурационный файл `/etc/opendkim.conf` следующие строки.

```conf
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
Они указывают соответсвие между доменом и ключем которым необходимо подписывать письмо.

```shell
# /etc/opendkim/keytable
ключ домен:селектор:/путь/до/ключа
```

```shell
# /etc/opendkim/signingtable
домен ключ
```

Например:

```shell
# /etc/opendkim/keytable
mail._domainkey.example.com example.com:mail:/etc/opendkim/mail.private
```

```
# /etc/opendkim/signingtable
example.com    mail._domainkey.example.com
```

### Настройка Postfix для работы с OpenDKIM

Указываем о необходимости подписывать все письма с помощью `dkim`.

```shell
$ sudo postconf -e milter_default_action=accept
$ sudo postconf -e milter_protocol=2
$ sudo postconf -e smtpd_milters=unix:/var/run/opendkim/opendkim.sock
$ sudo postconf -e non_smtpd_milters=unix:/var/run/opendkim/opendkim.sock
```

Перезапускаем службы и отправляем подписанное письмо.

```shell
$ sudo service postfix restart
$ sudo service opendkim restart
```

## Настроийки доменной зоны

Что бы сервер мог удостовериться в корректности подписи,
нужно добавить `TXT` запись содежащую ключ.

```shell
$ dig +short TXT mail._domainkey.example.com
"v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCvfTJ37Gqs06fhG0YYj/6HbojCrDp
F8X6u20YUaOax+jrvO0KtItfWYUi6hkCJeKbGTAOmqhWLu1T/DMt0XaICAJ7Q8525Z4ghwfvc5LgYyNSDEODeF
LNPlXgn3IP5o6Og2We/SnO4QCv8drKGf0N2xm5IIzIT8CjsbM6gPQIHTQIDAQAB"
```

Так же, хорошо указать разрешенные `ip` адреса для исходящих писем, в запись `spf`.

```shell
$ dig +short TXT example.com
"v=spf1 a:example.com ip4:<ip v4 addr> ip6:<ip v6 addr> ~all"
```

## Все не как у людей

Сегодня мы живем, в недалеком и почти светлом будущем, когда по бескрайним
просторам сети широко распространяется `ipv6` адресация. Но, оказывается,
абсолютно все письма отправленные с `ipv6` всегда воспринимаются гуглом, как спам.
Даже пройдя верефикацию по `dkim` и `spf` записям уходят в нежелательную почту.

Так что укажем в конфигурации `postfix` отправку только с использованием `ipv4`.

```shell
$ sudo postconf -e inet_protocols=ipv4
```

Теперь письма успешно доставляются, и проходят все валидации.

![gmail ok](/media/postfix/gmail_ok.png){.center .shadow}


## Django settings

Теперь можно подключить настройки `smtp` в джанго.

```python
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'info@example.com'
```
