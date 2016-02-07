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

Что бы правильно настроить `ssl` есть такая замечательная
[шпаргалка](https://mozilla.github.io/server-side-tls/ssl-config-generator/)
от `mozilla`.

В общем случае достаточно использовать следующие настройки:

```nginx
    listen 443 ssl;

    server_name example.com www.example.com;

    # certs sent to the client in SERVER HELLO are concatenated in ssl_certificate
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # intermediate configuration. tweak to your needs.
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_prefer_server_ciphers on;
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
# or
$ sudo nginx -s reload
```

Готово. Теперь вы можете открыть ваш сайт используя защищенное соединение.

##Автоматическое обновление сертификата

Сертификаты, которые выдает `Let's Encrypt`, действительны всего 90 дней.
В сравнениями с другими центрами сертификации, которые выдают
сертификаты на год.
Данный период кажется подозрительно коротким. Однако, в дальнейшем сроки
сертификатов планируют ещё сократить. Это сделано с целью уменьшения
угрозы от компрометации сертификата, а так же призывает повсеместно
использовать автопродление сертификата.

