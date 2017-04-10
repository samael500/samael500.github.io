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
[Aiohttp](http://aiohttp.readthedocs.io/en/stable/),
данные хранить в базе `PostgreSQL`, текущие сессии в `Redis`,
запросы проксировать через `Nginx`.

### Асинхронный фреймворк

Текущая версия `aiohttp 2.0.6`, однако оказалось что с ней не совместима
текущая версия `aiohttp debugtoolbar`
[issue #115](https://github.com/aio-libs/aiohttp-debugtoolbar/issues/115).
Так что будем использовать предыдущую версию `aiohttp 1.3.5`.

Простейшее приложение на `aiohttp` выглядит так:

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

### Шаблоны

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
