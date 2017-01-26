Title: Давайте шифровать!
Date: 2016-01-15 15:00
Modified: 2016-01-15 15:00
Category: Secure
Tags: letsencrypt, nginx, ssl, https, secure, git
Image: /media/letsencrypt/letsencrypt.jpg
Summary:
    `Let's Encrypt` представляет собой центр сертификации, который позволяет
    просто и **бесплатно** получить `TLS / SSL` сертификаты, тем самым
    позволяя использовать зашифрованное соединение `HTTPS`.
    В данный момент сервис находится на этапе бета тестирования, и получить
    сертификат в полностью автоматическом режиме, можно лишь при использовании
    веб-сервера `Apache`. Я предпочитаю использовать `nginx`, поэтому опишу
    как легко получить сертификат в ручном режиме.

`Let's Encrypt` представляет собой центр сертификации, который позволяет
просто и **бесплатно** получить `TLS / SSL` сертификаты, тем самым
позволяя использовать зашифрованное соединение `HTTPS`.
В данный момент сервис находится на этапе бета тестирования, и получить
сертификат в полностью автоматическом режиме, можно лишь при использовании
веб-сервера `Apache`. Я предпочитаю использовать `nginx`, поэтому опишу
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

##Подключение сертификата в nginx

Что бы правильно настроить `ssl` есть такая замечательная
[шпаргалка](https://mozilla.github.io/server-side-tls/ssl-config-generator/)
от `mozilla`.

В общем случае достаточно использовать следующие настройки:

```nginx
server {

    listen 443 ssl;

    server_name example.com www.example.com;

    # certs sent to the client in handshake are concatenated in ssl_certificate
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # secure configuration
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_prefer_server_ciphers on;

    # ...

}
```

Для перманентного перенаправления на защизенное соединение, нужно
создать дополнительный блок `server`.

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

После внесения изменений в настройки сервера, нужно не забыть перезагрузить
службу `nginx`.

```Bash
$ sudo service nginx restart
$ # or
$ sudo nginx -s reload
```

Готово. Теперь вы можете открыть ваш сайт используя защищенное соединение.

##Автоматическое обновление сертификата

Сертификаты, которые выдает `Let's Encrypt`, действительны всего 90 дней.
В сравнениями с другими центрами сертификации, которые выдают
сертификаты на год.
Данный период кажется подозрительно коротким. Однако, в дальнейшем сроки
сертификатов планируют ещё сократить. Это сделано с целью уменьшения
угрозы от компрометации приватного ключа, а так же призывает повсеместно
использовать автопродление сертификатов, в связи с тем, что через год,
можно и забыть его продлить.

Автопродление сертификата проходит с помощью плагина `webroot`, который для
верификации помещает специальный файл в директорию `./well-known`
доступную для чтения вебсервером.

```nginx
    location ~ /.well-known {
        root /path/to/root;
        allow all;
    }
```

Теперь мы можем использовать `letsencrypt-auto` с дополнительным параметром
`webroot-path`, передавая домены с помощью ключа `-d`:

```Bash
$ cd /opt/letsencrypt
$ ./letsencrypt-auto certonly -a webroot --agree-tos --renew-by-default \
    --webroot-path=/path/to/root -d example.com -d www.example.com
```

В результате обновления сертификата вы получите следующее сообщение:

```
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at
   /etc/letsencrypt/live/example.com/fullchain.pem. Your cert will
   expire on 2016-05-22. To obtain a new version of the certificate in
   the future, simply run Let's Encrypt again.
 - If you like Let's Encrypt, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

Получив обновленный сертификат, для его использования нужно перезапустить `nginx`

```Bash
$ sudo service nginx restart
$ # or
$ sudo nginx -s reload
```

Теперь создадим конфигурационный файл, для автоматической подстановки параметров.
Шаблон конфигурационного файла находится в примерах `letsencrypt`.

```Bash
$ cat /opt/letsencrypt/examples/cli.ini
# This is an example of the kind of things you can do in a configuration file.
# All flags used by the client can be configured here. Run Let's Encrypt with
# "--help" to learn more about the available options.

# Use a 4096 bit RSA key instead of 2048
rsa-key-size = 4096

# Uncomment and update to register with the specified e-mail address
# email = foo@example.com

# Uncomment and update to generate certificates for the specified
# domains.
# domains = example.com, www.example.com

# Uncomment to use a text interface instead of ncurses
# text = True

# Uncomment to use the standalone authenticator on port 443
# authenticator = standalone
# standalone-supported-challenges = tls-sni-01

# Uncomment to use the webroot authenticator. Replace webroot-path with the
# path to the public_html / webroot folder being served by your web server.
# authenticator = webroot
# webroot-path = /usr/share/nginx/html
```

Скопируем его в директорию `/usr/local/etc`:

```Bash
$ sudo cp /opt/letsencrypt/examples/cli.ini /usr/local/etc/le-renew-webroot.ini
```

Далее отредактируем его, изменив параметры `email`, `domains` и `webroot-path`.

```Bash
$ sudo nano /usr/local/etc/le-renew-webroot.ini

# This is an example of the kind of things you can do in a configuration file.
# All flags used by the client can be configured here. Run Let's Encrypt with
# "--help" to learn more about the available options.

# Use a 4096 bit RSA key instead of 2048
rsa-key-size = 4096

# Uncomment and update to register with the specified e-mail address
email = user@example.com

# Uncomment and update to generate certificates for the specified
# domains.
domains = example.com, www.example.com

# Uncomment to use a text interface instead of ncurses
# text = True

# Uncomment to use the standalone authenticator on port 443
# authenticator = standalone
# standalone-supported-challenges = tls-sni-01

# Uncomment to use the webroot authenticator. Replace webroot-path with the
# path to the public_html / webroot folder being served by your web server.
# authenticator = webroot
webroot-path = /path/to/root
```

Теперь, вместо того что бы указывать параметры с помощью ключей комманды
`letsencrypt`, мы можем использовать конфигурационный файл:

```Bash
$ cd /opt/letsencrypt
$ ./letsencrypt-auto certonly -a webroot --renew-by-default \
    --config /usr/local/etc/le-renew-webroot.ini
```

Скачаем и сделаем исполнимым скрипт автообновления сертификата.

```Bash
$ sudo curl -L -o /usr/local/sbin/le-renew-webroot \
    https://gist.githubusercontent.com/thisismitch/e1b603165523df66d5cc/raw/fbffbf358e96110d5566f13677d9bd5f4f65794c/le-renew-webroot
$ sudo chmod +x /usr/local/sbin/le-renew-webroot
```

Теперь если его выполнить, то будет выдано ссобщение, о том, что сертификат
не нуждается в обновлении.

```Bash
$ sudo le-renew-webroot
Checking expiration date for example.com...
The certificate is up to date, no need for renewal (89 days left).
```

Для того что бы скрипт регулярно проверял состояние сертификата добавим его
запуск в таблицу крона:

```Bash
$ sudo crontab -e
```

Добавим строчку, которая будет запускать скрипт каждое воскресенье в 5.30
утра, и логировать результат в файл `/var/log/le-renewal.log`:

```Bash
30 5 * * 7 /usr/local/sbin/le-renew-webroot >> /var/log/le-renewal.log
```

Теперь можно не беспокоится о сроке годности сертификата, он будет регулярно
обновлятся, когда будет приближаться срок истечения сертификата.
