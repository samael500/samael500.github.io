Title: Это Типограф
Date: 2015-10-13 15:00
Modified: 2015-10-13 15:00
Category: Python
Tags: python, artlebedev, typograf, django
Image: /media/browsers/pedestal.png
Status: draft
Summary:
    У студии Лебедева есть сервис типографирования текста, который
    так и называется [типограф](http://www.artlebedev.ru/tools/typograf/).
    Как заявляют сами разработчики, никто не напишет &laquo;Типограф&raquo;
    лучше них, в связи с чем они предлагают готовые
    [клиенты](http://www.artlebedev.ru/tools/typograf/webservice/)
    для работы c `api` данного сервиса...

В одном из проектов была поставлена задача типографировать текст
перед публикацией. Для этой задачи было решено использовать
&laquo;Типограф&raquo; Лебедева.

У студии Лебедева есть сервис типографирования текста, который
так и называется [типограф](http://www.artlebedev.ru/tools/typograf/).
Как заявляют сами разработчики, никто не напишет &laquo;Типограф&raquo;
лучше них, в связи с чем они предлагают готовые
[клиенты](http://www.artlebedev.ru/tools/typograf/webservice/)
для работы c `api` данного сервиса.

###Типограф клиент

Я не смотрел клиенты для других языков, но клиент для `Python`, который
студия Лебедева предлагает, откровенно сказать -- ужасен. В нем `xml` запрос
создается с помощью простой конкатенации строк и сомнительно экранирует
входные данные, `socket` подключается без таймлимита, что приводит к
бесконечно длительному ожиданию ответа, в случае если сервер недоступен.
Что уж говорить о рекомендациях `pep8`, которые там впринципе не соблюдаются.
Но самым существенным было то, что последнее изменение было сделано не вчера,
и даже не на прошлой неделе, а всего-ничего, от 24 мая 2007 года,
еще до релиза `Python 3.0`. Соответсвенно данный клиент не поддерживает
`Python 3.x`.

Проект был на `Python 3.4.2`, в связи с чем пришлось написать собсвтенный
клиент для работы с &laquo;Типографом&raquo;. Поскольку адекватного описания
`api` взаимодействия клиент-сервер в &laquo;Типографе&raquo; не приводится.
Так что все было сделано по аналогии со старым клиентом, вплоть до
наименований методов, лишь за исключением, что ненавистный мне
верблюжийРегистр был заменен змеиным_регистром.

Получившийся клиент для типографа доступен в `pypi`
[![typograf version](https://badge.fury.io/py/typograf.svg)](
https://pypi.python.org/pypi/typograf)

####Совместимость python 2.x и 3.x

Поскольку клиет типографа предельно простой, не хотелось нагружать его
дополнительными зависимостями, вроде [six](https://pypi.python.org/pypi/six)
для реализации совместимости версий `python`а, так что было использовано
`sys.version.startswith`.

```python
PY3 = sys.version.startswith('3.')
```

Единственными различиями между `py 2.x` и `py 3.x`, с которыми пришлось
столкнутся при написании клиента, это:

1. Во втором питоне, в сокет и из него отправляются строковые объекты,
а в третьем байтовые.
2. Файлы в памяти во втором питоне представлены объектами `StringIO.StringIO`,
а в третьем `io.BytesIO`.

Так что вся совместимость версий, свелась к двум-трем условиям вида:

```python
# ... import memory file stream

if PY3:
    from io import BytesIO as Container
else:
    from StringIO import StringIO as Container
```

```python
# ... calculate a length of request

length = len(soap_body.encode('utf-8')) if PY3 else len(soap_body)
```

```python
# ... convert to and from bytes for socket connection in py3

if PY3:  # convert to bytes
    soap_request = soap_request.encode('utf-8')

# ...
# take a response via socket
# ...

if PY3:  # convert to str
    response = response.decode()
```

####Socket timeout

Библиотека [socket](https://docs.python.org/library/socket.html)
предусматривает возможность установки максимального времени ожидания ответа
от сервера. Делается это с помощью метода `settimeout`.

```python
# send request use soket
connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connector.settimeout(self._timeout)
connector.connect((self.HOST, 80))
connector.sendall(soap_request)
# call for response
response = b''
buf = '0'
while len(buf):
    buf = connector.recv(8192)
    response += buf
connector.close()
```

В случае, если время ожидания превысит установленый таймаут, соединение будет
разорвано с вызовом исключения `socket.timeout: timed out`.

###Django Типограф

После реализации совместимого с `python 3.x` клиента было необходимо
прикрутить его к джанге.

####Быстрое решение

Так как проект был уже запущен в продакшен, нужно было быстро подключить
типографирование. Типографировать нужно было всего две модели, поэтому была
создана простая функция `make_typograf`, вызов которой был повешен на сигнал
сохранения моделей.

```python
# helpers/service.py

def make_typograf(instance, fields):
    """ For each instance.field in fields - make typograf """
    typograf = RemoteTypograf()
    for field in fields:
        instance.__dict__[field] = typograf.try_process_text(instance.__dict__[field])
    return instance
```

```python
# articles/signals.py

from django.db.models.signals import pre_save
from articles.models import Article
from helpers.service import make_typograf

def typograf(sender, instance, **kwargs):
    make_typograf(instance, ('title', 'subtitle', ))

pre_save.connect(typograf, sender=Article)
```

```python
# cards/signals.py

from django.db.models.signals import pre_save
from cards.models import Card
from helpers.service import make_typograf

def typograf(sender, instance, **kwargs):
    make_typograf(instance, ('person_profession', 'soldier_rank', 'history', ))

pre_save.connect(typograf, sender=Card)
```

Данный подход имел ряд недостатков:

1. В случае если бы было неоходимо добавить новую модель,
то потребовалось бы дописывать ещё один сигнал.
2. Модель "типографировалась" при каждом сохранении, не зависимо от изменения
самого текста, что приводило к лишним запросам на сервис Лебедева при каждом
сохранении.
3. Наиболее существенный недостаток. Модераторы начали жаловаться на то,
что текст становится невозможно проверять, из за `html` сущностей,
которые затрудняют чтение. (см. пример ниже)

Пример исходного текста:
```
"Вы все еще кое-как верстаете в "Ворде"? - Тогда мы идем к вам!"
```

Пример типографированного текста:
```
<p>&laquo;Вы&nbsp;все еще кое-как верстаете в&nbsp;&bdquo;Ворде&ldquo;?
&mdash;&nbsp;Тогда мы&nbsp;идем к&nbsp;вам!&raquo;<br />
</p>
```

Пример результата:

> <p>&laquo;Вы&nbsp;все еще кое-как верстаете в&nbsp;&bdquo;Ворде&ldquo;?
> &mdash;&nbsp;Тогда мы&nbsp;идем к&nbsp;вам!&raquo;<br />
> </p>

####Ненавязчивый типограф

Для решения указанных недостатков было решено создать пакет `django-typograf`
[![django-typograf version](https://badge.fury.io/py/django-typograf.svg)](
https://pypi.python.org/pypi/django-typograf), который позволил бы
автоматически типографировать указанные поля в моделях, делал это только
вслучае необходимости и не влиял на отображение исходного текста в
административном интефейсе.

Для того чтобы не влиять на исходный текст, будем использовать
дополнительные поля, которые будут хранить в себе оттипографированный текст.
Для того чтобы не отправлять на типографирование текст каждый раз, без
явной на то необходимости, будем хранить хешированное значение исходного
текста и сравнивать его изменения.

#####Хешсумма

Поскольку нам не важно какой вид будет иметь хешсумма, сравним
производительность различных алгоритмов хеширования с целью выбора
оптимального.

Затраты времени для `md5` суммы:
```bash
$ time python -c 'from hashlib import md5
for i in xrange(int(1e+6)): md5(str(i)).hexdigest()'

real    0m1.015s
user    0m1.006s
sys 0m0.008s
```

Затраты времени для `sha1` суммы:
```bash
$ time python -c 'from hashlib import sha1
for i in xrange(int(1e+6)): sha1(str(i)).hexdigest()'

real    0m1.095s
user    0m1.090s
sys 0m0.004s
```

Затраты времени для `crc32` суммы:
```bash
$ time python -c 'from binascii import crc32
for i in xrange(int(1e+6)): crc32(str(i))'

real    0m0.473s
user    0m0.472s
sys 0m0.000s
```

Затрат времени на стравнение строк:
```bash
$ time python -c 'for i in xrange(int(1e+6)): "123" == "321"'

real    0m0.092s
user    0m0.087s
sys 0m0.008s
```

Затрат времени на стравнение целых чисел:
```bash
$ time python -c 'for i in xrange(int(1e+6)): 123 == 321'

real    0m0.088s
user    0m0.080s
sys 0m0.008s
```

Таким образом, для хеширования используем алгоритм `crc32` из библиотеки
[binascii](https://docs.python.org/library/binascii.html), так как это очень
быстрая хешсумма, а также результат вычислений можно сохранить в
целочисленное поле базы данных, что выгоднее чем строка, как с точки зрения
затрат памяти, так и с точки зрения времени сравнения.

Несмотря на то, что целочисленные значения дают дополнительное преимущество в
затратах скорости и памяти, на практике всеравно будем использовать строковое
представлениет. Так как, в `python 3.x` алгоритм `crc32` возвращает результат
в диапазоне `unsigned int: 0 .. 4294967295`, а в `python 2.x` в диапазоне
`int: -2147483648 .. 2147483647`. Целочисленное поле `PostgreSQL` способно
разместить только диапазон `int`, даже джанговское поле `PositiveIntegerField`
не расширяет диапазон до `2 ** 32 - 1`, а сокращает его ровно в половину до
`0 .. 2147483647`.

#####Скрытые поля

Служебные поля для типографированного текста и хешсуммы будут создаваться
автоматически с помощью метода метакласса предка.

```python
    # ...

    @classmethod
    def create_typograf_fields(cls, local_typograf_fields, attrs):
        """Create helpers to the local typografed fields """
        for field_name in local_typograf_fields:
            # check is text field
            field = attrs[field_name]
            if not isinstance(field, (models.CharField, models.TextField)):
                raise TypografFieldError(
                    'Can\'t be typografed field "{field}".'
                    ' This must be a text or char field.'.format(field=field_name))
            # create fields for store typografed text and typografed hash
            typograf_field = models.TextField(blank=True, null=True)
            typograf_field.creation_counter += 0.0001
            typograf_field_hash = models.CharField(max_length=32, blank=True, null=True)
            typograf_field_hash.creation_counter += 0.0001
            # create fields name's
            typograf_field_name = get_typograf_field_name(field_name)
            typograf_field_hash_name = get_typograf_hash_field_name(field_name)
            # update attrs
            attrs.update({
                typograf_field_name: typograf_field,
                typograf_field_hash_name: typograf_field_hash})

        return attrs
```

В данном методе для каждого поля из спика `local_typograf_fields`,
который задается в атрибутах метакласса модели наследника, создается по два
служебных поля, вида `typograf_{field}` и `typograf_{field}_hash`.

Для того чтобы эти служебные поля были недоступны в административном
интерфейсе, добавим внутренний метод `_exclude`, который будет возвращать
списки скрытых полей.

```python
from django.contrib import admin
from django_typograf.utils import get_typograf_field_name, get_typograf_hash_field_name

class TypografAdmin(admin.ModelAdmin):

    """ Admin class for hide typograf fields from admin site """

    def _exclude(self, obj=None):
        """ Mark typograf fields as exclude """
        exclude = ()
        if obj:
            exclude += tuple((
                get_typograf_field_name(field) for field in obj._meta.typografed_fields))
            exclude += tuple((
                get_typograf_hash_field_name(field) for field in obj._meta.typografed_fields))
        return exclude

    def get_form(self, request, obj=None, **kwargs):
        exclude = self.exclude or ()
        exclude += self._exclude(obj)
        kwargs.update(dict(exclude=exclude))
        return super().get_form(request, obj, **kwargs)
```

####Использования типографа

Теперь, для автоматического типографирования текста, достаточно установить
пакет `django_typograf` из `pypi`, наследовать модель от `TypografModel`
и указать поля, которые необходимо типографировать.

```python
# articles/models.py

from django.db import models
from django_typograf.models import TypografModel

class Article(TypografModel):

    """ Model for articles """

    title = models.CharField(verbose_name='заголовок', max_length=200)
    subtitle = models.CharField(verbose_name='подзаголовок', max_length=200)
    site_url = models.URLField(verbose_name='URL')

    class Meta(Sortable.Meta):
        typograf = ('title', 'subtitle', )
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
```

А также, в шаблоне, не забыть работать с "типографированными" полями.

```
<h1>{{ article.typograf_title|default_if_none:article.title|safe }}</h1>
<h2>{{ article.typograf_subtitle|default_if_none:article.subtitle|safe }}</h2>
```
