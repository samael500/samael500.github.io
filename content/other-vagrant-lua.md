Title: Собственное хранилище версированных Vagrant боксов с помощью Nginx и Lua
Date: 2016-10-25 15:00
Modified: 2016-10-25 15:00
Category: Другое
Tags: vagrant, lua, nginx, self-hosted, wb-tech, best
Image: /media/lua-vagrant/lua-vagrant.png
Image_width: 1280
Image_height: 791
Summary:
    Для удобного процесса разработки, быстрого переключения между проектами и
    эффективного взаимодействия бэкенд и фронтенд команд. Мы, в
    [WB--Tech](http://wbtech.pro/), работаем в виртуальном окружении
    [Vagrant](https://www.vagrantup.com/) + [VirtualBox](https://www.virtualbox.org/).
    `Vagrant` -- прекрасный менеджер окружения, а для ускорения развертывания
    виртуальной машины можно использовать компилированные, версированные боксы.
    Хостить их можно на [родном сервере](https://atlas.hashicorp.com/boxes/search),
    но триал `Vagrant enterprise` у нас закончился, в связи с чем было решено
    хостить боксы самостоятельно. А сделали мы это с помощью [Lua](https://www.lua.org/).

Для удобного процесса разработки, быстрого переключения между проектами и
эффективного взаимодействия бэкенд и фронтенд команд. Мы, в
[WB--Tech](http://wbtech.pro/), работаем в виртуальном окружении
[Vagrant](https://www.vagrantup.com/) + [VirtualBox](https://www.virtualbox.org/).
`Vagrant` -- прекрасный менеджер окружения, а для ускорения развертывания
виртуальной машины можно использовать компилированные, версированные боксы.
Хостить их можно на [родном сервере](https://atlas.hashicorp.com/boxes/search),
но триал `Vagrant enterprise` у нас закончился, в связи с чем было решено
хостить боксы самостоятельно. А сделали мы это с помощью [Lua](https://www.lua.org/).

Версийность боксов в `Vagrant` описывается при помощи `json`
[документа](https://www.vagrantup.com/docs/boxes/format.html).

```json
{
    "name": "box_name",
    "description": "This box description.",
    "versions": [
        {
            "version": "42.0",
            "providers": [
                {
                    "name": "virtualbox",
                    "url": "http://somewhere.com/precise64_010_virtualbox.box",
                    "checksum_type": "sha1",
                    "checksum": "foo"
                }
            ]
        }
    ]
}
```

Далее, в самом `Vagrantfile` нужно указывать путь к метаданным в атрибуте `config.vm.box_url`:

```ruby
config.vm.box = "box_name"
config.vm.box_version = "42.0"
config.vm.box_url = "http://somewhere.com/path/to/metadata.json"
```

Каждый раз при обновлении версии бокса, описывать данный документ вручную, а
потом загружать на сервер вместе с новым боксом, было бы слишком скучно.
Делать для этого какой либо бэкенд нецелесообразно. Когда можно обойтись одним
лишь `Nginx` с дополнительным [модулем](https://www.nginx.com/resources/wiki/modules/lua/).
Так что формирование метаданных сделано при помощи простого скрипта на `Lua`.

### Далеко ли до Луны?

`Lua` (с порт. — "луна") — скриптовый язык программирования,
разработанный в подразделении `Tecgraf` Католического университета
Рио-де-Жанейро. Интерпретатор языка является свободно
распространяемым, с открытыми исходными текстами на языке Си.

По возможностям, идеологии и реализации язык ближе всего к `JavaScript`,
однако `Lua` отличается более мощными и гораздо более гибкими конструкциями.
Хотя `Lua` не содержит понятия класса и объекта в явном виде,
механизмы объектно-ориентированного программирования, включая множественное
наследование, легко реализуются с использованием метатаблиц, которые также
отвечают за перегрузку операций и т. п. Реализуемая модель
объектно-ориентированного программирования — прототипная (как и в `JavaScript`).

### Установка и зависимости

Описание приведено для операционных систем семейства `Debian`.

- Прежде всего нам потребуется `Nginx` с модулем
[lua-nginx-module](https://github.com/openresty/lua-nginx-module).
Собрать его можно вручную, но проще установить готовый пакет
[nginx-extras](https://packages.debian.org/ru/sid/nginx-extras),
который содержит множество полезных модулей.
- Также не будет лишним интерпретатор `Lua`, чтобы оттестировать скрипт
в интерактивной консоли.
- Для компиляции модулей, потребуется утилита `make`.
- Время собирать лунные камни, нам будет нужен менеджер пакетов [luarocks](https://luarocks.org/).
    - Для поиска файлов в директории, будем использовать модуль [luaposix](http://luaposix.github.io/luaposix/).
    - Ну и для конвертации словаря в `JSON` установим [JSON4Lua](http://json.luaforge.net/).

```shell
$ sudo apt-get -y install make nginx-extras lua5.1 luarocks
$ # install lua modules
$ sudo luarocks install luaposix
$ sudo luarocks install JSON4Lua
```

### Здравствуй, подлунный мир!

"Здравствуй, мир!" на `Lua`, так же прост и прекрасен, как и на `Python`.

```Lua
Lua 5.1.5  Copyright (C) 1994-2012 Lua.org, PUC-Rio
> print "Hello world!"
Hello world!
```

Теперь попробуем тоже самое при помощи полнофункционального
[Nginx Lua API](https://github.com/openresty/lua-nginx-module#nginx-api-for-lua).

```Nginx
server {
    listen    80;

    location /hello-world {
        content_by_lua '
            ngx.header.content_type = "text/plain"
            ngx.say("Hello world!")
        ';
    }
}
```

```shell
$ curl http://10.1.1.111/hello-world
Hello world!
```

Для исполнения `Lua` скрипта, служит директива `content_by_lua`,
для которого `Nginx` ожидает получить ответ через `API`. Если скрипт большой,
то не обязательно описывать его внутри конфига, достаточно лишь подключить
через директиву `content_by_lua_file`.

### Vagrant метаданные

#### Настройка Nginx

На сервере мы складываем боксы в директорию `hosted`, создавая поддиректорию
для каждого проекта. Сами боксы в которой хранятся файлами со строго указанным
форматом имени `{provider}-{version.subversion}.box`.

Формируя примерно такое дерево:

```shell
$ tree hosted/
hosted/
├── foo
│   ├── docker-1.0.box
│   ├── docker-1.3.box
│   ├── virtualbox-1.0.box
│   ├── virtualbox-1.4.box
│   └── virtualbox-1.7.box
└── bar
    ├── virtualbox-1.0.box
    ├── virtualbox-1.1.box
    └── virtualbox-1.2.box

2 directories, 8 files
```

Настроим `nginx` так, чтобы для любого бокса -- начиналось непосредственное скачивание,
а для имени проекта, возвращались вычисленные метаданные.

```Nginx
server {
    listen    80;

    set $box_url 'http://10.1.1.111/%s/%s-%s.box';
    set $box_prefix '/home/vagrant/proj/hosted/';

    location ~ /*\.box$ {
        root /home/vagrant/proj/hosted;
        # just return box
    }

    location ~ /(?<box_name>\w+)/?$ {
        content_by_lua_file /home/vagrant/proj/app/handler.lua;
    }
}
```

Переменные `$box_url` и `$box_prefix` будут использовать при формировании метаданных.

#### Вычисление метаданных с помощью Lua

Приступим теперь непосредственно к формированию метаданных
для версирования `Vagrant` боксов.

Идея будет заключаться в том, что по запросу, `Lua` будет осуществлять поиск
сохраненных боксов в заданной директории на сервере, вычислять их хешсуммы,
и формировать ответ в формате метаданных `vagrant`а.

Используя [glob](https://luaposix.github.io/luaposix/modules/posix.glob.html)
из библиотеки `posix` найдем все боксы.

```Lua
local box_root = ngx.var.box_prefix .. ngx.var.box_name .. '/'
local posix = require "posix"
local glob = posix.glob (box_root .. '*.box')

-- Если боксы не найдены, можно сразу возвращать 404
if not glob then
    ngx.status = ngx.HTTP_NOT_FOUND
    return ngx.exit (ngx.HTTP_NOT_FOUND)
end
```

Итеративно пройдем по найденным боксам, и сформируем словарь с найденными версиями.

```Lua
local versions = {}
-- Discover the boxes
for _, box in ipairs (glob) do
    -- Обрабатываем найденый бокс, определяя версию и формируя описание
    local provider, version = make_provider (box)
    if version then
        if versions[version] == nil then
            -- Если версия встречается впервые, создаем запись для новой версии
            versions[version] = {
                version = version,
                providers = {provider}
            }
        else
            -- Если версия уже была описана, обновляем список провайдеров
            table.insert (versions[version]['providers'], provider)
        end
    end
end
```

Для вычисления хешсуммы больших файлов боксов воспользуемся утилитами операционной системы.
Такими как `sha1sum`, `sha256sum`, `md5sum`...
Делается это с помощью вызова процесса через `io.popen`:

```Lua
local hash = 'sha1'

function get_hash (filepath)
    -- Вычисляем хешсумму используя вызов консольной утилиты sha1sum
    local command = string.format ('%ssum %s | cut -d " " -f1', hash, filepath)
    local hashsum = assert (io.popen (command, 'r'))
    local result = string.gsub (hashsum:read ('*a'), '\n', '')
    hashsum:close ()
    return result
end
```

Функция `make_provider` выполняется для каждого найденного бокса.
Подразумевается, что боксы хранятся на сервере со строго заданным форматом имени:
`{provider}-{version.subversion}.box`

Разбираем версию и имя провайдера, регуляркой, после чего формируем словарь,
описывающий данный бокс.

```Lua
local function make_provider (filepath)
    -- Make vagrant provider from given file
    local box_provider, box_version = string.match (
        filepath, string.format ('%s(%%a+)-(.+).box', box_root))
    return {
        -- Название провайдера virtualbox или docker
        name = box_provider,
        -- Прямая ссылка на бокс, которую будет запрашивать vagrant
        url = string.format (ngx.var.box_url, ngx.var.box_name, box_provider, box_version),
        -- Алгоритм хешсуммы sha1, sha256, md5
        checksum_type = hash,
        -- Строка со значением хешсуммы
        checksum = get_hash(filepath)
    }, box_version
end
```

Обработав все боксы и сформировав список версий, обернем всё в дополнительный словарь.

```Lua
-- Make result response
local vagrant = {
    name = ngx.var.box_name,
    description = string.format ("Boxes for %s proj", ngx.var.box_name),
    versions = {}
}
for _, version in pairs (versions) do
    table.insert (vagrant['versions'], version)
end
```

Ответ сервера `JSON` с найденными версиями.

```Lua
ngx.header.content_type = "application/json; charset=utf-8"
local json = require "json"
ngx.say (json.encode (vagrant))
```

### Лунное затмение (вместо заключения)

Полученный скрипт формирует `JSON` ответ содержащий метаинформацию о боксах.

```shell
$ curl http://10.1.1.111/example | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   943    0   943    0     0  13412      0 --:--:-- --:--:-- --:--:-- 13471
```
```json
{
  "versions": [
    {
      "version": "1.7",
      "providers": [
        {
          "url": "http://10.1.1.111/example/virtualbox-1.7.box",
          "checksum": "3221c0fd58a4b2430efc5eeaf09cb8eaf877f3a9",
          "name": "virtualbox",
          "checksum_type": "sha1"
        }
      ]
    },
    {
      "version": "1.3",
      "providers": [
        {
          "url": "http://10.1.1.111/example/docker-1.3.box",
          "checksum": "def7148aa7ded879dbf5944af4785c2b09aba97a",
          "name": "docker",
          "checksum_type": "sha1"
        }
      ]
    },
    {
      "version": "1.4",
      "providers": [
        {
          "url": "http://10.1.1.111/example/virtualbox-1.4.box",
          "checksum": "63b06d8c065f5c2522c356d4d6ceb718ec3f8198",
          "name": "virtualbox",
          "checksum_type": "sha1"
        }
      ]
    },
    {
      "version": "1.0",
      "providers": [
        {
          "url": "http://10.1.1.111/example/docker-1.0.box",
          "checksum": "65cb550765d251604dcfeedc36ea61f66ce205c4",
          "name": "docker",
          "checksum_type": "sha1"
        },
        {
          "url": "http://10.1.1.111/example/virtualbox-1.0.box",
          "checksum": "c0a9d5c3d6679cfcc4b1374e3ad42465f3dd596e",
          "name": "virtualbox",
          "checksum_type": "sha1"
        }
      ]
    }
  ],
  "name": "example",
  "description": "Boxes for example proj"
}
```

Полный пример скрипта можно посмотреть в репозитории на
[github](https://github.com/Samael500/ngx-vagrant). А при желании
поиграться запустив настроенный `Vagrant`.

О том, как ещё можно интересно использовать связку `Nginx` и `Lua`, можно
прочитать в статье [Применение Nginx + Lua для обработки контактной формы](http://dizballanze.com/drugoe/primenenie-nginx-lua-dlia-obrabotki-prostykh-form/)
