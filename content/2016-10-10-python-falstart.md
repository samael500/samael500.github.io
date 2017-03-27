Title: Быстрый старт на Джанго
Date: 2016-10-10 15:00
Modified: 2016-10-10 15:00
Category: Python
Tags: python, github, django, vagrant, wb-tech, falstart, best
Image: /media/falstart/falstart.png
Image_width: 1280
Image_height: 791
Summary:
    Новый проект это всегда интересно, новые задачи, новый опыт,
    новые знания. Начиная новый проект хочется сразу броситься "в бой".
    Но перед этим приходится тратить время на первоначальную настройку
    окружения, подключения и установку зависимостей, создания структуры,
    инициализацию проекта. Порой это может занимать целый день. Рутинная,
    и во многом однообразная задача написания `fab` скриптов для запуска
    виртуального окружения -- охлаждает пыл и отвлекает. Для того чтобы
    пропускать этот шаг, и сразу приступать к разработке, был написан
    простенький `fab` скрипт для фальстарта нового проекта.
    Так что теперь, достаточно написать `falstart <название проекта>`,
    выпить чашечку чая и приступать к работе над новым проектом.

Новый проект это всегда интересно, новые задачи, новый опыт, новые знания.
Начиная новый проект хочется сразу броситься "в бой". Но перед этим приходится
тратить время на первоначальную настройку окружения, подключения и установку
зависимостей, создания структуры, инициализацию проекта. Порой это может
занимать целый день. Рутинная и во многом однообразная задача написания `fab`
скриптов для запуска виртуального окружения -- охлаждает пыл и отвлекает.
Для того чтобы пропускать этот шаг, и сразу приступать к разработке.
Был написан простенький `fab` скрипт для фальстарта нового проекта.
Так что теперь, достаточно написать `falstart <название проекта>`,
выпить чашечку чая и приступать к работе над новым проектом.

Мы, в [WB--Tech](http://wbtech.pro/) в основном используем следующий стек:
[Python 3.x](https://www.python.org/) + [Django](https://www.djangoproject.com/) +
[PostgreSQL](https://www.postgresql.org/) + [Celery](http://www.celeryproject.org/) +
[Redis](http://redis.io/).

А саму разработку ведем в виртуальном окружении [Vagrant](https://www.vagrantup.com/) +
[VirtualBox](https://www.virtualbox.org/) под управлением
[OS Debian](https://www.debian.org/index.html).

![falstart](/media/falstart/fs-logo.png){.center}

[Falstart](https://github.com/Samael500/falstart) позволяет быстро развернуть
виртуальное окружение и приступить к работе ответив на десяток простых вопросов.

```Shell
$ falstart awesome
> Django version ['1.9.5'] 1.10.2
> Debian version (for vagrant box) ['jessie64']
> Python version ['3.5.1'] 3.5.2
> Vagrant box IP-addr ['10.1.1.123'] 10.1.1.111
> Do you nead a POSTGRES? [Y/n]
> Do you nead a CELERY? [y/N] y
> Do you nead a REDIS? [y/N] y
> Do you nead a SENTRY? [y/N]
> Database name ['awesome_db']
> Database user ['awesome_user']
> Database pass ['vFeH1uJVN']
```

После чего выполняются скрипты и через 10-15 минут будет готова структура проекта.

### Пред зависимости
Для работы фальстарта необходим [Vagrant](https://www.vagrantup.com/) и [VirtualBox](https://www.virtualbox.org/)

### Установка
Фальстарт доступен для установки через `pip`

```shell
$ pip install falstart
```

### Результат

Пример результата: [falstart-example](https://github.com/Samael500/falstart-example).

<details>
    <summary>Пример итоговой структуры проекта</summary>
```shell
$ tree
.
├── awesome
│   ├── celery.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── celery.cpython-35.pyc
│   │   ├── __init__.cpython-35.pyc
│   │   ├── settings.cpython-35.pyc
│   │   ├── settings_local.cpython-35.pyc
│   │   ├── urls.cpython-35.pyc
│   │   └── wsgi.cpython-35.pyc
│   ├── settings_local.py
│   ├── settings_local.py.example
│   ├── settings.py
│   ├── static
│   │   └── admin
│   │       ├── css
│   │       │   ├── base.css
│   │       │   ├── changelists.css
│   │       │   ├── dashboard.css
│   │       │   ├── fonts.css
│   │       │   ├── forms.css
│   │       │   ├── login.css
│   │       │   ├── rtl.css
│   │       │   └── widgets.css
│   │       ├── fonts
│   │       │   ├── LICENSE.txt
│   │       │   ├── README.txt
│   │       │   ├── Roboto-Bold-webfont.woff
│   │       │   ├── Roboto-Light-webfont.woff
│   │       │   └── Roboto-Regular-webfont.woff
│   │       ├── img
│   │       │   ├── calendar-icons.svg
│   │       │   ├── gis
│   │       │   │   ├── move_vertex_off.svg
│   │       │   │   └── move_vertex_on.svg
│   │       │   ├── icon-addlink.svg
│   │       │   ├── icon-alert.svg
│   │       │   ├── icon-calendar.svg
│   │       │   ├── icon-changelink.svg
│   │       │   ├── icon-clock.svg
│   │       │   ├── icon-deletelink.svg
│   │       │   ├── icon-no.svg
│   │       │   ├── icon-unknown-alt.svg
│   │       │   ├── icon-unknown.svg
│   │       │   ├── icon-yes.svg
│   │       │   ├── inline-delete.svg
│   │       │   ├── LICENSE
│   │       │   ├── README.txt
│   │       │   ├── search.svg
│   │       │   ├── selector-icons.svg
│   │       │   ├── sorting-icons.svg
│   │       │   ├── tooltag-add.svg
│   │       │   └── tooltag-arrowright.svg
│   │       └── js
│   │           ├── actions.js
│   │           ├── actions.min.js
│   │           ├── admin
│   │           │   ├── DateTimeShortcuts.js
│   │           │   └── RelatedObjectLookups.js
│   │           ├── calendar.js
│   │           ├── cancel.js
│   │           ├── change_form.js
│   │           ├── collapse.js
│   │           ├── collapse.min.js
│   │           ├── core.js
│   │           ├── inlines.js
│   │           ├── inlines.min.js
│   │           ├── jquery.init.js
│   │           ├── popup_response.js
│   │           ├── prepopulate_init.js
│   │           ├── prepopulate.js
│   │           ├── prepopulate.min.js
│   │           ├── SelectBox.js
│   │           ├── SelectFilter2.js
│   │           ├── timeparse.js
│   │           ├── urlify.js
│   │           └── vendor
│   │               ├── jquery
│   │               │   ├── jquery.js
│   │               │   ├── jquery.min.js
│   │               │   └── LICENSE-JQUERY.txt
│   │               └── xregexp
│   │                   ├── LICENSE-XREGEXP.txt
│   │                   ├── xregexp.js
│   │                   └── xregexp.min.js
│   ├── urls.py
│   └── wsgi.py
├── Makefile
├── manage.py
├── provision
│   ├── fabric_provisioner.py
│   ├── fabric_provisioner.pyc
│   └── templates
│       ├── environment.j2
│       ├── locale.gen.j2
│       └── nginx-host.j2
├── requirements-remote.txt
├── requirements.txt
├── Vagrantfile
├── var
│   ├── celery_awesome_worker.log
│   ├── celery_awesome_worker.pid
│   ├── celerybeat-schedule
│   └── gunicorn.pid
└── wheels
    ├── amqp-1.4.9-py2.py3-none-any.whl
    ├── anyjson-0.3.3-py3-none-any.whl
    ├── billiard-3.3.0.23-py3-none-any.whl
    ├── celery-3.1.23-py2.py3-none-any.whl
    ├── coverage-4.2-cp35-cp35m-linux_x86_64.whl
    ├── coverage_badge-0.1.2-py3-none-any.whl
    ├── Django-1.10.2-py2.py3-none-any.whl
    ├── django_rainbowtests-0.5.1-py3-none-any.whl
    ├── gunicorn-19.4.5-py2.py3-none-any.whl
    ├── kombu-3.0.37-py2.py3-none-any.whl
    ├── mccabe-0.4.0-py2.py3-none-any.whl
    ├── pep257-0.7.0-py2.py3-none-any.whl
    ├── pep8-1.7.0-py2.py3-none-any.whl
    ├── psycopg2-2.6.1-cp35-cp35m-linux_x86_64.whl
    ├── pyflakes-1.0.0-py2.py3-none-any.whl
    ├── pylama-7.0.7-py2.py3-none-any.whl
    ├── pytz-2016.7-py2.py3-none-any.whl
    └── redis-2.10.5-py2.py3-none-any.whl
```
</details>

Теперь можно перейти по адресу указанному в приветственном сообщении `Vagrant`а
и увидеть начальную страницу Джанго.

```shell
==> awesome_vagrant: Machine 'awesome_vagrant' has a post `vagrant up` message. This is a message
==> awesome_vagrant: from the creator of the Vagrantfile, and not from Vagrant itself:
==> awesome_vagrant:
==> awesome_vagrant: awesome dev server successfuly started.
==> awesome_vagrant:     Connect to host with:
==> awesome_vagrant:     http://10.1.1.111/
==> awesome_vagrant:     or over ssh with `vagrant ssh`
==> awesome_vagrant:
==> awesome_vagrant:     Admin user credentials:
==> awesome_vagrant:       login: root
==> awesome_vagrant:       password: 123123
==> awesome_vagrant:
```

![init app](/media/falstart/init_app.png){.center}
