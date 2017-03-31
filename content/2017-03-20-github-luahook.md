Title: Обработка вебхуков GitHub с помощью Nginx и Lua
Date: 2017-03-20 15:00
Modified: 2017-03-31 15:00
Category: Github
Tags: github, lua, nginx, webhook, autodeploy
Image: /media/luahook/luahook.png
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


Проверка корректности запроса. В первую очередь,
нужно убедится что запрос действительно `POST`.
Сделаем это с помощью функции
[req.get_method](https://github.com/openresty/lua-nginx-module#ngxreqget_method).

```lua
    -- should be POST method
    if ngx.req.get_method() ~= "POST" then
        ngx.log(ngx.ERR, "wrong event request method: ", ngx.req.get_method())
        return ngx.exit (ngx.HTTP_NOT_ALLOWED)
    end
```

Следующим шагом проверим, что это запрос содержит заголовок с хук методом.
Получив все заголовки с помощью функции
[req.get_headers](https://github.com/openresty/lua-nginx-module#ngxreqget_headers).

```lua
    local event = 'push'

    -- ...

    local headers = ngx.req.get_headers()
    -- with correct header
    if headers['X-GitHub-Event'] ~= event then
        ngx.log(ngx.ERR, "wrong event type: ", headers['X-GitHub-Event'])
        return ngx.exit (ngx.HTTP_NOT_ACCEPTABLE)
    end
```

Так как мы будем слушать вебхуки в формате `json` -- проверим контент тип запроса.

```lua
    -- should be json encoded request
    if headers['Content-Type'] ~= 'application/json' then
        ngx.log(ngx.ERR, "wrong content type header: ", headers['Content-Type'])
        return ngx.exit (ngx.HTTP_NOT_ACCEPTABLE)
    end

```

По первичным признакам, запрос корректный. Проанализируем тело запроса.
С помощью функций
[req.read_body](https://github.com/openresty/lua-nginx-module#ngxreqread_body) и
[req.get_body_data](https://github.com/openresty/lua-nginx-module#ngxreqget_body_data).


```lua
    -- read request body
    ngx.req.read_body()
    local data = ngx.req.get_body_data()

    if not data then
        ngx.log(ngx.ERR, "failed to get request body")
        return ngx.exit (ngx.HTTP_BAD_REQUEST)
    end
```

Проверим корректность подписи запроса, которая передается в заголовке `X-Hub-Signature`.

```lua
    -- validate GH signature
    if not verify_signature(headers['X-Hub-Signature'], data) then
        ngx.log(ngx.ERR, "wrong webhook signature")
        return ngx.exit (ngx.HTTP_FORBIDDEN)
    end
```

```
    data = json.decode(data)
    -- on master branch
    if data['ref'] ~= branch then
        ngx.say("Skip branch ", data['ref'])
        return ngx.exit (ngx.HTTP_OK)
    end
```
