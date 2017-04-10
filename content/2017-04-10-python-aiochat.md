Title: Простой чат на AioHTTP
Date: 2017-04-10 15:00
Modified: 2017-04-10 15:00
Category: Python
Tags: python, async, asyncio, aiohttp, github, chat, tutorial
Image: /media/aiochat/lua-github.png
Image_width: 1280
Image_height: 791
Summary:
    В повседневной работе я тесно связан с `Python 3`, но такие его замечательные
    возможности, как асинхронность [asyncio](https://docs.python.org/3/library/asyncio.html)
    и синтаксический сахар [PEP 492](https://www.python.org/dev/peps/pep-0492/)
    использовать не приходится. Из асинхронных задач сталкиваюсь только с `Celery`,
    но это не совсем та асинхронность, скорее бэкграунд
    с очередью задач выполняемых воркерами синхронно. Пришло время исправить это,
    и поближе познакомится с асинхронностью в `Python 3.5+`. Сделаем это
    на примере простого чата с комнатами.

В повседневной работе я тесно связан с `Python 3`, но такие его замечательные
возможности, как асинхронность [asyncio](https://docs.python.org/3/library/asyncio.html)
и синтаксический сахар [PEP 492](https://www.python.org/dev/peps/pep-0492/)
использовать не приходится. Из асинхронных задач сталкиваюсь только с `Celery`,
но это не совсем та асинхронность, скорее бэкграунд
с очередью задач выполняемых воркерами синхронно. Пришло время исправить это,
и поближе познакомится с асинхронностью в `Python 3.5+`. Сделаем это
на примере простого чата с комнатами.

### Постановка задачи

Реализовать простой асинхронный чат с комнатами на `WebSocket`-ах.

Необходимый функционал:

- Создать пользователя или авторизоваться под существующим.
- Создать комнату, или подключится к уже существующей.
- Иметь возможность видеть всю историю чат комнаты.
    В том числе, подключения и отключения пользователей от комнаты.
- Администрирование комнаты.

### Технологии

Для реализации чата будем использовать `Python 3.6` и фреймворк
[AioHTTP](http://aiohttp.readthedocs.io/en/stable/),
данные хранить в базе `PostgreSQL`, текущие сессии в `Redis`,
запросы проксировать через `Nginx`.

### Асинхронный фреймворк

Текущая версия `AioHTTP 2.0.6`, однако оказалось что с ней не совместима
текущая версия `AioHTTP debugtoolbar`
[issue #115](https://github.com/aio-libs/aiohttp-debugtoolbar/issues/115).
Так что будем использовать предыдущую версию `AioHTTP 1.3.5`.

Простейшее приложение на `AioHTTP` выглядит так:

```python3
from aiohttp import web

async def handler(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.router.add_route('GET', '/', handler)
app.router.add_route('GET', '/{name}', handler)

web.run_app(app)
```

Как можно заметить, роуты конфигурируются после инициализации приложения.
`Url` аргументы, задаются подобно форматированию строк `{slug}`.

В момент создания приложения, можно указать `middlewares`, передав
их в конструктор приложения.

```python3
app = web.Application(loop=loop, middlewares=middlewares)
```

### База данных и модели

В качестве базы данных используем `PostgreSQL`, для работы с которой воспользуемся
[PeeWee ORM](http://docs.peewee-orm.com/en/latest/) и асинхронным менеджером,
[PeeWee Async](https://peewee-async.readthedocs.io/en/latest/).

Создадим базовую модель, с неинициализированной базой.
Саму базу инициализируем в момент конфигурирования приложения.


```python3
import peewee
import peewee_async


database = peewee_async.PostgresqlDatabase(None)


class BaseModel(peewee.Model):

    """ Base model with db Meta """

    class Meta:
        database = database
```

```python3
import peewee_async
from helpers.models import database

DATABASE = {
    'database': 'aiochat',
    'password': 'supersecret',
    'user': 'aiochat_user',
    'host': 'localhost',
}

# ...

database.init(**DATABASE)
app.database = database
app.database.set_allow_sync(False)
app.objects = peewee_async.Manager(app.database)
```

Сама идея Менеджера базы данных -- взята из `Django`, но в `pee wee async`
работает это немного подругому, и с непривычки вызывает недоумение.

> High-level API provides a single point for all async ORM calls.
> Meet the Manager class! The idea of Manager originally comes from Django,
> but it’s redesigned to meet new asyncio patterns.

```python3
# Django manager
user = User.objects.get(username__iexact='Alice')

# Pee Wee manager
user = await objects.get(User, User.username ** 'Alice')
```

Через менеджер вызываются асинхронные запросы,
но через контекст можно провести синхронный запрос, например создание таблицы.

```python3
with objects.allow_sync():
    User.create_table(True)
```

### Шаблоны и пути

В качестве шаблонизатора будем использовать
[асинхронную jinja2](http://aiohttp-jinja2.readthedocs.io/en/stable/).

Конфигурируется точно также, как и синхронная версия.

```python3
import jinja2
import aiohttp_jinja2

# ...

jinja_env = aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR),
    context_processors=[aiohttp_jinja2.request_processor], )
```

Рендер шаблона, изящно спрятан в декоратор для вьюхи.

```python3
import aiohttp_jinja2
from aiohttp import web

class Index(web.View):

    @aiohttp_jinja2.template('template_name.html')
    async def get(self):
        # return context for render
        return {'foo': 'boo'}
```

Routes, как уже было сказано выше, конфигурируются после инициализации приложения.
Через функциию `app.router.add_route`. Несмотря на то что статику у нас будет
отдавать `Nginx`, задаем её специальным роутом `add_static`, чтобы в шаблонах
иметь возможность подключать статические файлы.

```python3
# urls.py
from accounts.urls import routes as accounts_routes
from chat.urls import routes as chat_routes

from views import Index

routes = (
    dict(method='GET', path='/', handler=Index, name='index'),
    * accounts_routes,
    * chat_routes,
)
```

```python3
# app.py
from urls import routes
for route in routes:
    app.router.add_route(**route)
app.router.add_static('/static', settings.STATIC_DIR, name='static')
```

В шаблоне получаем доступ к роутам, через объект `app`.

```jinja2
<a href="{{ app.router['index'].url_for() }}">Main page</a>

<link href="{{ app.router.static.url(filename='chat.css') }}" rel="stylesheet">
<script src="{{ app.router.static.url(filename='chat.js') }}"></script>
```

### Сессии

Для работы с сессиями будем использовать
[aiohttp session](http://aiohttp-session.readthedocs.io/en/latest/).
Данная библиотека позволяет на выбор, работать с `cookies` или `redis` хранилищами.
Мне больше нравится `redis`. Для подключения потребуется библиотека
[aioredis](https://aioredis.readthedocs.io/en/v0.3.0/).

Подключим сессии и редис.

```python3
import aioredis

from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage

# ...

redis_pool = await aioredis.create_pool(settings.REDIS_CON, loop=loop)
middlewares = [session_middleware(RedisStorage(redis_pool))]
```

Что бы получить текущюю сессию, нужно дождаться ответа из корутины `get_session`.
Мне нравится подход в джанго, когда в каждом объекте Запрос,
есть прямой доступ к сессии и пользователю.
Сделаем подобное в `aiohttp` с помощью `middlewares`.

```python3
from aiohttp_session import get_session
from accounts.models import User


async def request_user_middleware(app, handler):
    async def middleware(request):
        request.session = await get_session(request)
        request.user = None
        user_id = request.session.get('user')
        if user_id is not None:
            request.user = await request.app.objects.get(User, id=user_id)
        return await handler(request)
    return middleware
```

Раз уж у нас есть объект пользователя в запросе, создадим декораторы
для ограничения доступа авторизованным и анонимным пользователям.

```python3
from aiohttp import web
from helpres.tools import redirect

def login_required(func):
    """ Allow only auth users """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is None:
            redirect(self.request, 'login')
        return await func(self, *args, **kwargs)
    return wrapped


def anonymous_required(func):
    """ Allow only anonymous users """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is not None:
            redirect(self.request, 'index')
        return await func(self, *args, **kwargs)
    return wrapped
```

В данных декораторах используем функцию `redirect`, она вызывает исключение
которое пораждает редирект. В `AioHTTP` можно вызвать лобой из
[web исключений](https://github.com/aio-libs/aiohttp/blob/master/aiohttp/web_exceptions.py)
это сделано круче чем в `Django`, где есть возможность вернуть только
`404`, `403` и `400` через исключения `Http404`, `PermissionDenied`,
`SuspiciousOperation` соответсвенно. А редирект должен быть отдан явным ответом.

```python3
from aiohttp import web

def redirect(request, router_name, *, permanent=False, **kwargs):
    """ Redirect to given URL name """
    url = request.app.router[router_name].url(**kwargs)
    if permanent:
        raise web.HTTPMovedPermanently(url)
    raise web.HTTPFound(url)
```

### WebSockets

В `Aiohttp` реализованы вебсокеты, через `web.WebSocketResponse()`,
работа с ними практически не отличается от обычных вьюх.
Добавляется асинхронный цикл пока соединение активно.

```python3
async def wshandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.MsgType.text:
            await ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.MsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break

    return ws
```

Для хранения текущих соединений, и разсылки бродкаст сообщений,
будем использовать объект `app`.


```python3
ws = web.WebSocketResponse()
await ws.prepare(self.request)
request.app.wslist.append(ws)

# ...

async def broadcast(self, message):
    """ Send messages to all in this room """
    for peer in self.request.app.wslist:
        peer.send_json(message.as_dict())
```

Поумолчанию `Nginx` не проксирует заголовки `Upgrade` и `Connection`,
которые используются при переключении на `WS` запрос.

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    # ...

    location / {
        proxy_pass          http://localhost:8000;
        proxy_set_header    Host $host;
        proxy_set_header    X-Real-IP $remote_addr;

        # ws support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 1h;
    }
}
```

### Тестирование

Тестировать приложение `AioHTTP` можно разными способами.
Мне нравиться подход [Unittest](http://aiohttp.readthedocs.io/en/stable/testing.html#unittest).
Единственная особенность, нужно добавить метод `get_application`
и объявлять асинхронные тесты, декарируя их через `unittest_run_loop`.

```python3

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from app import create_app


class AioChatTestCase(AioHTTPTestCase):

    """ Base test case for aiochat """

    async def get_application(self, loop):
        """ Return current app """
        serv_generator, handler, app = await create_app(loop)
        return app


class IndexTestCase(AioChatTestCase):

    """ Testing index app views """

    url_name = 'index'

    def setUp(self):
        super().setUp()
        self.url = self.app.router[self.url_name].url_for()

    @unittest_run_loop
    async def test_url_reversed(self):
        """ Url should be / """
        self.assertEqual(str(self.app.router[self.url_name].url_for()), '/')
        self.assertEqual(str(self.url), '/')

    @unittest_run_loop
    async def test_index(self):
        """ Should get 200 on index page """
        response = await self.client.get('/')
        self.assertEqual(response.status, 200)
        content = await response.text()
        self.assertIn('Simple asyncio chat', content)
```

### Функциональная часть

Основная функциональность чата - передача сообщений клиентам в пределах комнаты.

```python3

class WebSocket(web.View):

    """ Process WS connections """

    async def broadcast(self, message):
        """ Send messages to all in this room """
        for peer in self.request.app.wslist[self.room.id].values():
            peer.send_json(message.as_dict())

    async def get(self):
        self.room = await get_object_or_404(
            self.request, Room, name=self.request.match_info['slug'].lower())
        user = self.request.user
        app = self.request.app

        # При подключении создаем WebSocketResponse
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        if self.room.id not in app.wslist:
            # Создаем пустую комнату если ещё нет
            app.wslist[self.room.id] = {}

        # Сохраняем соединение в объекте app и создаем сервисное сообщение
        app.wslist[self.room.id][user.username] = ws
        message = await app.objects.create(
            Message, room=self.room, user=None, text=f'{user} join chat room')

        # Разсылка всем подключенным клиентам
        await self.broadcast(message)

        # В асинхронном цикле слушаем сообщения от текущего сокета
        async for msg in ws:
            if msg.tp == MsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    # Сохраняем сообщение в базу и шлем бродкаст
                    message = await app.objects.create(
                        Message, room=self.room, user=user, text=text)
                    await self.broadcast(message)

        # Когда соединение закрывается, удаляем пользователя из сохраненных соединений
        app.wslist.pop(user.username, None)

        # Сервисное сообщение об отключении в бродкаст
        message = await app.objects.create(
            Message, room=self.room, user=None, text=f'{user} left chat room')
        await self.broadcast(message)

        # возвращаем WebSocketResponse
        return ws
```

В качестве администрирования комнаты, добавим возможность выполнять команды
пользователей. Возьмем две простые команды,
`очистить историю комнаты` и `удалить пользователя из комнаты`.

```python3
    async def command(self, cmd):
        """ Run chat command """
        app = self.request.app
        if cmd.startswith('/kill'):
            # unconnect user from room
            try:
                target = cmd.split(' ')[1]
                # Найдем пользователя по имени и отключим от чата
                peer = app.wslist[self.room.id][target]
                await self.disconnect(target, peer, silent=True)
            except KeyError:
                pass
        elif cmd == '/clear':
            # Удалим все сообщения из комнаты
            count = await app.objects.execute(
                Message.delete().where(Message.room == self.room))
            # В бродкаст вышлем пользователям команды для очистки истории на клиенте
            for peer in app.wslist[self.room.id].values():
                peer.send_json({'cmd': 'empty'})
        elif cmd == '/help':
            # Вспомогательная команда для отображения справки
            return {'text': dedent('''\
                - /help - display this msg
                - /kill {username} - remove user from room
                - /clear - empty all messages in room
                ''')}
        else:
            return {'text': 'wrong cmd {cmd}'}
```

В асинхронном цикле будем сравнивать, если сообщение начинается с `/`
значит обрабатывать его как команду.

```python3
    text = msg.data.strip()
    if text.startswith('/'):
        ans = await self.command(text)
        if ans is not None:
            ws.send_json(ans)
    else:
        message = await app.objects.create(Message, room=self.room, user=user, text=text)
        await self.broadcast(message)
```

### Клиент

Браузерный клиент это простое `WebSocket` подключение, с определенными
командами на отправку и отображение сообщений.

```js
var sock = new WebSocket('ws://' + window.location.host + WS_URL);

function showMessage(message) {
    /* Append message to chat area */
    console.log(message);
    var data = jQuery.parseJSON(message.data);
    $messagesContainer.append('<li class="media">' + data.text + '</li>');
    $chatArea.scrollTop($messagesContainer.height());
}

// ...

$('#send').on('submit', function (event) {
    event.preventDefault();
    var $message = $(event.target).find('input[name="text"]');
    sock.send($message.val());
    $message.val('').focus();
});

sock.onopen = function (event) {
    console.log(event);
    console.log('Connection to server started');
};

sock.onclose = function (event) {
    console.log(event);
    if(event.wasClean){
        console.log('Clean connection end');
    } else {
        console.log('Connection broken');
    }
    window.location.assign('/');
};

sock.onerror = function (error) {
    console.log(error);
};

sock.onmessage = showMessage;

```

### Результат и критика

Как выяснилось, асинхронный код в `Python 3` практически
не отличается от синхронного. Работать с ним легко и весело. `WebSocket`
вызывает отдельный восторг, позволяя отправлять сообщения клиентам со стороны
сервера, без явного запроса.

`AioHTTP` позволяет легко реализовать простой асинхронный сервер с `WebSocket`ами.
Но что то большое я бы не стал на на нем писать, иначе всё начнет превращатся в рутину-корутины.

Полный пример чата можно посмотреть в репозитории на `github`
[Samael500/aiochat](https://github.com/Samael500/aiochat). А при желании
поиграться запустив настроенный `Vagrant`.

Данный чат создан исключительно в ознакомительных целях, поэтому имеет ряд допущений.

- У меня возникла сложность с созданием тестовой базы данных через
`pee wee async`, поэтому тесты весьма поверхностные.
Только что бы обозначить общий подход к тестированию.
- Регистрация и авторизация пользователей, без паролей и каких либо подтверждений.
- Каждый пользователь имеет полные права администрирования комнат.
- Нет нормальной валидации форм на создание пользователя или комнаты.
- Команды чата реализованы без валидации формата команды.
- История комнаты отдается без паджинации вся полностью, при хоть сколь либо
большом числе комнат/пользователей/сообщение, эти запросы будут выполнятся
долго, создавая нагрузку как на сервер так и на клиент.
- Подключения вебсокетов хранятся в едином объекте `APP`, что тоже создает
лишние проблеммы при большом числе полдключений и комнат.
Рационально в данном случае разпараллеливать комнаты между разными инстансами
приложения.
