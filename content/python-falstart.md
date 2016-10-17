Title: Быстрый старт на Джанго
Date: 2016-10-10 15:00
Modified: 2016-10-10 15:00
Category: Python
Tags: python, github, django, vagrant, falstart
Image: /media/teamcity-coverage/banner.jpg
Image_width: 735
Image_height: 455
Summary:
    Новый проект это всегда интерестно, новые задачи, новый опыт,
    новые знания. Начиная новый проект хочется сразу броситься "в бой".
    Но перед этим приходится тратить время на первоначальную настройку
    окружения, подключения и установку зависимостей, создания структуры,
    инициализацию проекта. Порой это может занимать целый день. Рутинная,
    и во многом однообразная задача написания `fab` скриптов для запуска
    виртуального окружения -- охлаждает пыл и отвлекает. Для того что бы
    пропускать этот шаг, и сразу приступать к разработке, был написан
    простенький `fab` скрипт для фальстарта нового проекта.

Новый проект это всегда интерестно, новые задачи, новый опыт, новые знания.
Начиная новый проект хочется сразу броситься "в бой". Но перед этим приходится
тратить время на первоначальную настройку окружения, подключения и установку
зависимостей, создания структуры, инициализацию проекта. Порой это может
занимать целый день. Рутинная и во многом однообразная задача написания `fab`
скриптов для запуска виртуального окружения -- охлаждает пыл и отвлекает.
Для того что бы пропускать этот шаг, и сразу приступать к разработке.
Был написан простенький `fab` скрипт для фальстарта нового проекта.

Мы, в [WB--Tech](http://wbtech.pro/) в основном используем следующий стек:

[Python 3.x](https://www.python.org/) + [Django](https://www.djangoproject.com/) +
[PostgreSQL](https://www.postgresql.org/) + [Celery](http://www.celeryproject.org/) +
[Redis](http://redis.io/).

А саму разработку ведем в виртуальном окружении [Vagrant](vagrantup.com) +
[VirtualBox](https://www.virtualbox.org/) под управлением
[OS Debian](https://www.debian.org/index.html).

[Falstart](https://github.com/Samael500/falstart) позволяет быстро развернуть
виртуальное окружение и приступить к работе ответив на десяток простых вопросов:

```Shell
$ falstart falstart-example
> Django version ['1.9.5'] 1.10.2
> Debian version (for vagrant box) ['jessie64']
> Python version ['3.5.1'] 3.5.2
> Vagrant box IP-addr ['10.1.1.123'] 10.1.1.111
> Do you nead a POSTGRES? [Y/n]
> Do you nead a CELERY? [y/N] y
> Do you nead a REDIS? [y/N] y
> Do you nead a SENTRY? [y/N] y
> Database name ['falstartexample_db']
> Database user ['falstartexample_user']
> Database pass ['VJJxu87Ki']
```
