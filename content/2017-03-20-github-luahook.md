Title: Обработка вебхуков GitHub с помощью Nginx и Lua
Date: 2017-03-20 15:00
Modified: 2017-03-31 15:00
Category: Github
Tags: github, lua, nginx, webhook, autodeploy
Image: /media/luahook/luahook.png
Image_width: 1280
Image_height: 791
Summary:
    После того, как принимается `pull-request` и наработки кода попадают в
    мастер. Нужно обновить сервер, выполнив на нем комманды деплоя.
    Обычно у нас эта обязанность возложена на сервер `CI TeamCity`,
    который в случае успешного билда мастер ветки накатывает изменения
    на продакшен сервера. Но иногда не нужно такое взаимодействие,
    а достаточно просто знать факт пуша в мастер,
    и обработать его самостоятельно.
    С помощью вебхуков `GitHub` может уведомлять о
    [push](https://developer.github.com/v3/activity/events/types/#pushevent)
    событиях в репозитории.
    Но для валидации и обработки этих запросов, нужен какой-либо бекенд.
    В этом нам помогает знакомая связка `Nginx` + `Lua`.

После того, как принимается `pull-request` и наработки кода попадают в
мастер. Нужно обновить сервер, выполнив на нем комманды деплоя.
Обычно у нас эта обязанность возложена на сервер `CI TeamCity`,
который в случае успешного билда мастер ветки накатывает изменения
на продакшен сервера. Но иногда не нужно такое взаимодействие,
а достаточно просто знать факт пуша в мастер,
и обработать его самостоятельно.
С помощью вебхуков `GitHub` может уведомлять о
[push](https://developer.github.com/v3/activity/events/types/#pushevent)
событиях в репозитории.
Но для валидации и обработки этих запросов, нужен какой-либо бекенд.
В этом нам помогает знакомая связка `Nginx` + `Lua`.

### Предварительная настройка

Нам понадобятся `Nginx` с модулем [lua-nginx-module](https://github.com/openresty/lua-nginx-module).
И две дополнительные библиотеки для `lua`. Для того чтобы прочесть `json`
тело запроса используем [JSON4Lua](http://json.luaforge.net/), а для
валидации подписи [LuaCrypto](http://mkottman.github.io/luacrypto/).
Установим их через менеджер пакетов [luarocks](https://luarocks.org/).

```shell
$ sudo luarocks install JSON4Lua
$ sudo luarocks install luacrypto
```

Подробнее о том, как настроить `Nginx` и `Lua` можно прочитать в 
[статье](|filename|/2016-10-25-other-vagrant-lua.md#ustanovka-i-zavisimosti).

### Валидация запроса

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

Проверим корректность подписи запроса, которая передается в заголовке
`X-Hub-Signature`, используя функцию [verify_signature](#proverka-podpisi).

```lua
-- validate GH signature
if not verify_signature(headers['X-Hub-Signature'], data) then
    ngx.log(ngx.ERR, "wrong webhook signature")
    return ngx.exit (ngx.HTTP_FORBIDDEN)
end
```

Последним шагом, убедимся что этот `push` был в интересующую нас ветку.
Разобрав тело запроса в таблицу `lua` с помощью функции
[json.decode](http://json.luaforge.net/#json_decode).

```lua
local branch = 'refs/heads/master'

-- ...

data = json.decode(data)
-- on master branch
if data['ref'] ~= branch then
    ngx.say("Skip branch ", data['ref'])
    return ngx.exit (ngx.HTTP_OK)
end
```

#### Проверка подписи

Для подтверждения корректности запроса, `GitHub` использует `HMAC` `SHA1` подпись, и передает её в заголовке
`X-Hub-Signature` пример в [документации](https://developer.github.com/webhooks/securing/#validating-payloads-from-github).

Вызовем функцию [crypto.hmac.digest](http://luacrypto.luaforge.net/0.1/luacrypto.html#usage-hmac)
и сравним её результат с полученным заголовком.

```lua
local secret = '<MY SUPER SECRET>'

-- ...

local function verify_signature (hub_sign, data)
    local sign = 'sha1=' .. crypto.hmac.digest('sha1', data, secret)
    return hub_sign == sign
end
```

#### Константное сравнение строк

Простое сравнение строк на `==` использовать не рекомендуется, т.к.
злоумышленник может провести [атаку по времени](https://en.wikipedia.org/wiki/Timing_attack).

В `lua` нельзя просто так взять, и обратиться к строке по индексу.
Так что, для удобства внедрим данную функцию в метакласс строки.

```lua
getmetatable('').__index = function (str, i)
    return string.sub(str, i, i)
end
```

Напишем функцию сравнения строк за "константное" время.
Строки равны тогда и только тогда, когда равны посимвольно.

```lua
local function const_eq (a, b)
    -- Check is string equals, constant time exec
    local equal = string.len(a) == string.len(b)
    for i = 1, math.min(string.len(a), string.len(b)) do
        equal = (a[i] == b[i]) and equal
    end
    return equal
end
```

### Автоматический деплой

В случае, если `webhook` прошел все валидации, можно ему доверять.
Через системный вызов [io.popen](https://www.lua.org/manual/5.1/manual.html#pdf-io.popen)
выполним необходимые комманды деплоя. В данном примере осуществляется
простой `pull` из репозитория.

```lua
local function deploy ()
    local handle = io.popen("cd /path/to/repo && sudo -u username git pull")
    local result = handle:read("*a")
    handle:close()

    ngx.say (result)
    return ngx.exit (ngx.HTTP_OK)
end
```

Полный пример `handler`а можно посмотреть
в [gist](https://gist.github.com/Samael500/5dbdf6d55838f841a08eb7847ad1c926)
или вопросе на [StackOverflow](http://stackoverflow.com/a/43146712/4716629).
