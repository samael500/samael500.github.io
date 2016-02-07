Title: Давайте шифровать!
Date: 2016-01-15 15:00
Modified: 2016-01-15 15:00
Status: draft
Category: Secure
Tags: letsencrypt, nginx, ssl, https, secure, git
Image: /media/wrong-exif/wrong_exif.png
Summary:
    `Let's Encrypt` представляет собой центр сертификации, который позволяет
    просто и **бесплатно** получить `TLS / SSL` сертификаты, тем самым
    позволяя использовать зашифрованное соединение `HTTPS`.
    В данный момент сервис находится на этапе бета тестирования, и получить
    сертификат в полностью автоматическом режиме, можно лишь при использовании
    веб-сервера `Apache`. Я предпочитаю использовать `Nginx`, поэтому опишу
    как легко получить сертификат в ручном режиме.

`Let's Encrypt` представляет собой центр сертификации, который позволяет
просто и **бесплатно** получить `TLS / SSL` сертификаты, тем самым
позволяя использовать зашифрованное соединение `HTTPS`.
В данный момент сервис находится на этапе бета тестирования, и получить
сертификат в полностью автоматическом режиме, можно лишь при использовании
веб-сервера `Apache`. Я предпочитаю использовать `Nginx`, поэтому опишу
как легко получить сертификат в ручном режиме.

##Получение сертификата Let's Encrypt

`Let's Encrypt` устанавливается просто клонируя репозиторий.

```Bash
$ sudo git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt
$ cd cd /opt/letsencrypt
```

Теперь получим сертификат используя следующую команду:

```Bash
$ ./letsencrypt-auto certonly --standalone
```

Для данной команды необходимы привелегии суперпользователя, так что возможно
будет потребован ввод пароля.

Поскольку для проверки домена производитсья запрос на 80 порт,
то он должен быть свободен.

![nginx error](/media/letsencrypt/nginx.png){.center}

Что бы освободить порт, можно временно остановить `nginx` выполнив команду:

```Bash
$ sudo service nginx stop
```

`letsencrypt` запрашивает адрес электронной почты для
уведомлений или востановления ключей.

![email](/media/letsencrypt/email.png){.center}

Далее, предлагают согласиться с условиями использования сервиса.

![agree](/media/letsencrypt/agree.png){.center}

После, нужно указать для какого домена создается сертифика. Включая
все необходимые поддомены.

![domain](/media/letsencrypt/domain.png){.center}

При успешном получении сертификата, выдается следующее сообщение:

```
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at
   /etc/letsencrypt/live/you.domain.com/fullchain.pem. Your cert
   will expire on 2016-15-06. To obtain a new version of the
   certificate in the future, simply run Let's Encrypt again.
 - If you like Let's Encrypt, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

После успешного получения сертификата у вас будут следующие файлы:

- cert.pem: Сертификат домена
- chain.pem: Let's Encrypt сертификат
- fullchain.pem: cert.pem и chain.pem объединенные
- privkey.pem: Ключ сертификата

Что бы проверить что сертификаты успешно созданы и доступны,
выведите содержимое директории `/etc/letsencrypt/live/your_domain_name`,
где `your_domain_name` имя вашего домена.

```Bash
$ sudo ls /etc/letsencrypt/live/your_domain_name
```

##Подключение сертификата в Nginx

