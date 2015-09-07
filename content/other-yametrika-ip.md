Title: Определение IP адреса посетителя в отчетах Yandex Метрика
Date: 2015-09-13 15:00
Modified: 2015-09-13 15:00
Category: Другое
Status: draft
Tags: ip, javascript, yandex, metrika, watch
Image: /media/google-ban/google_ban.png
Summary:
    Обновленная метрика не отображает информацию об `ip` адресе посетителей
    сайта, сделано это с целью обезличивания статистики посещений. Данная
    [новость](http://clubs.ya.ru/metrika/replies.xml?item_no=10888) была
    официально озвучена в клубе метрики. Обезличивание это здорово, но порой
    хочется узнать действительно ли в статистике отображаются различные
    посетители, или же это одно и тот же лицо, которое заходит с разных
    браузеров или устройств.

Обновленная метрика не отображает информацию об `ip` адресе посетителей
сайта, сделано это с целью обезличивания статистики посещений. Данная
[новость](http://clubs.ya.ru/metrika/replies.xml?item_no=10888) была
официально озвучена в клубе метрики. Обезличивание это здорово, но порой
хочется узнать действительно ли в статистике отображаются различные
посетители, или же это одно и тот же лицо, которое заходит с разных
браузеров или устройств.

Также различным рекламщикам, может быть интересна информация об `ip` адресах,
например, с целью вычисления ботов скликеров. 

К счастью, метрика достаточно гибкая и позволяет устанавливать
пользовательские параметры, тем самым создавать специальный
персонализированный отчет о действиях пользователей. Благодаря чему,
мы можем привязать информацию об `ip` адресе к конкретному визиту. 

##Параметры визитов yandex.метрика

Сервис [параметры визитов](https://yandex.ru/support/metrika/reports/visit-params.xml)
позволяет прикрепить к информации о посещении `json` словарь с дополнительными
параметрами. Для этого необходимо в конструктор счетчика добавить аргумент
`params` с необходимыми значениями.

Например, если информация об `ip` адресе будет содержаться в переменой
`userip`, то словарь параметры может выглядеть следующим образом:

```javascript
{
    'ip': userip
}
```

Конструктор счетчика, в таком случае, будет выглядеть так:

```javascript
    w.yaCounterXXXXXX = new Ya.Metrika({
        id:XXXXXX,
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true,
        params:{'ip': userip}
    });
```

Где `XXXXXX` идентификатор счетчика.

Чтобы просмотреть полученные результаты необходимо перейти: `метрика` &rarr;
`отчеты` &rarr; `стандартные отчеты` &rarr; `содержание` &rarr;
`параметры визитов`

![visit params path](/media/yametrika-ip/visit_params_path.png){.center .shadow}

![visit params detail](/media/yametrika-ip/visit_params_detail.png){.center .shadow}

Но, сами по себе `ip` адреса не столь информативны, интерестнее просмотреть
связь посещения и `ip` адреса в вебвизоре. Для этого в вебвизор нужно добавить
столбец "Параметры".

![webvisor col params](/media/yametrika-ip/webvisor_col_params.png){.center .shadow}

![webvisor ip detail](/media/yametrika-ip/webvisor_ip_detail.png){.center .shadow}

##Определение IP адреса

Выше я упоминал о переменной в которой содержится `ip` адрес посетителя.
Задать эту переменную легко если Вы имеете доступ к бэкэнду.

Например в `django`, предварительно подключив
`django.core.context_processors.request`:

```html
<script type="text/javascript">
    var userip = "{{ request.META.REMOTE_ADDR }}";
</script>
```

Или, если Вы используете проксирование:

```html
<script type="text/javascript">
    var userip = "{{ request.META.HTTP_X_REAL_IP }}";
</script>
```

Или, например, в `php`:

```html
<script type="text/javascript">
    var userip = "<? echo $_SERVER['REMOTE_ADDR'];?>";
</script>
```

Но что если сайт статический и какой либо бэкэнд отсутствует? В таком случае
можно воспользоваться сервисом [l2.io](https://l2.io), который позволяет
получить `ip` на клиенте. К примеру Ваш `ip` адрес:
**<script type="text/javascript" src="https://www.l2.io/ip.js"></script>**

Чтобы задать `ip` адрес в переменную, нужно вставить такой скрипт:

```html
<script type="text/javascript" src="https://www.l2.io/ip.js?var=userip"></script>
```

Полный фрагмент скрипта яндекс метрики будет выглядеть так:

```html
<!-- получаем ip адрес одним из указанных вариантов -->
<script type="text/javascript" src="https://www.l2.io/ip.js?var=userip"></script>
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function (d, w, c) {
        (w[c] = w[c] || []).push(function() {
            try {
                w.yaCounterXXXXXX = new Ya.Metrika({
                    id:XXXXXX,
                    clickmap:true,
                    trackLinks:true,
                    accurateTrackBounce:true,
                    webvisor:true,
                    params:{'ip': userip}
                });
            } catch(e) { }
        });
    // продолжение счетчика
    // ...
</script>
<!-- /Yandex.Metrika counter -->
```
