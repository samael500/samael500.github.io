Title: Три года в команде
Date: 2017-01-15 15:00
Modified: 2017-01-15 15:00
Category: Другое
Tags: wb-tech
Image: /media/lua-vagrant/lua-vagrant.png
Image_width: 1280
Image_height: 791
Summary:
    Кажется ещё только вчера я был студентом, но вот уже пролетело три года,
    как я работаю в дружной и слаженной команде [Вебтек](http://wbtech.pro)...

Кажется ещё только вчера я был студентом, но вот уже пролетело три года,
как я работаю в дружной и слаженной команде [Вебтек](http://wbtech.pro).

![wbt team](/media/wbt3/team.jpg){.center}

Началось всё в конце 2013 года, я тогда учился на 1-м курсе магистратуры,
а знания `python` были весьма поверхностными.

Мне предложили пройти стажировку в вебтек, а для поступления -- выполнить
простое тестовое задание, создать сайт на `django` с парой моделей и
несколькими вьюхами. Даже сохранился репозиторий с этим заданием
[github.com:Samael500/todo-test-task](https://github.com/Samael500/todo-test-task).

Заканчивался семестр, нужно было сдавать зачеты, а впереди предстояли
новогодние каникулы, на которые я уехал к своей девушке. А по-возвращению
пошел на практику в [1С-Рарус](http://rarus.ru/), где занятия проходили
с утра до вечера. Так что выполнение тестового задания слегка затянулось,
более чем на месяц. Примерно, на третий день в рарусе, я вспомнил о тестовом
заданрии, и наконец решил его сделать. К тому-же срок уже поджимал.

В то время, я плохо знал `python`, не сталкивался с `django`, не было опыта
работы с `linux` и `git`. Но взяв за основу
[django tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/),
за несколько дней тестовое задание было полностью готово.
За одним исключением -- не было произведено ни одного коммита.
Пришло время закоммитить результаты работы, и, как говорится -- ничего не предвещало беды.

```shell
$ git add .
$ git status
$ # тут оказался длинный список не нужных файлов, т.к. я забыл доавить .gitignore
$ # я решил удалить лишнее, но вместо git reset, я совершил ошибку
$ git rm -rf
$ git add .
$ git status
$ # всё пропало, всё что нажито непосильным трудом...
```

Было и смешно, и грусно одновременно, но ничего, пришлось сделать
тестовое задание с нуля, заново. Во второй раз я справился всего за пол дня.
И уже более аккуратно подходил к контролю версий.

После проверки тестового задания, меня взяли на испытательный срок,
а в дальнейшем и на постоянную работу.

За эти три года работы в [wb-tech](http://wbtech.pro), я узнал много нового
и получил практический опыт разработки.
Поучаствовал в создании и поддержке многих проектов.

<details>
    <summary>Некоторые из которых представлены ниже:</summary>

Каталог реалитишоу Мир реалити.

`Django`, `Postgre`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="http://mirreality.ru/">
        <img src="/media/wbt3/mirreality.png" class="center" alt="mirreality">
    </a>
</div>

<hr />

Площадка для купли-продажи запчастей для автомобилей в Казани.

`Django`, `Postgre`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="http://autokazan.ru/">
        <img src="/media/wbt3/autokazan.png" class="center" alt="autokazan">
    </a>
</div>

<hr />

Сервис создания скришотов вебстраниц Coment.me.

`Flask`, `PhantomJS`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="http://coment.me/">
        <img src="/media/wbt3/coment.png" class="center" alt="coment">
    </a>
</div>

<hr />

Спецпроект Ленты к юбилею победы в Великой отечественной войне. Победа 70.

`Django`, `Postgre`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="http://pobeda70.lenta.ru/">
        <img src="/media/wbt3/may9.png" class="center" alt="pobeda70">
    </a>
</div>

<hr />

Сервис проектирования каркасных домов.

`Flask`, `MongoDB`, `Celery`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="#">
        <img src="/media/wbt3/fhouse.png" class="center" alt="fhouse">
    </a>
</div>

<hr />

Визуализация науки от команды Visual-Science.

`Yii`, `MySQL`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="http://visual-science.com/">
        <img src="/media/wbt3/visual.png" class="center" alt="visual">
    </a>
</div>

<hr />

Геоинформационная система поиска оптимальной точки размещения коммерческого объекта.

`Django`, `Postgre`, `PostGIS`, `Geoserver`, `Celery`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="https://arendohod.ru/">
        <img src="/media/wbt3/arend.png" class="center" alt="arend">
    </a>
</div>

<hr />

Увлекательные путешествия по России и миру. Pro Adventure.

`Django`, `Postgre`, `Celery`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="https://pro-adventure.ru/">
        <img src="/media/wbt3/pro.png" class="center" alt="pro">
    </a>
</div>

<hr />

Площадка для купли-продаже брендовой одежды. Preloved.

`Django`, `Postgre`, `Celery`.

<div class="center browser-mockup with-url" style="width:75%">
    <a href="#">
        <img src="/media/wbt3/plvd.png" class="center" alt="plvd">
    </a>
</div>

</details>

