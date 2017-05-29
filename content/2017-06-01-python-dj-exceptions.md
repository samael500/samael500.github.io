Title: WEB исключения в Django
Date: 2017-06-01 15:00
Modified: 2017-06-01 15:00
Category: Python
Tags: django, exceptions, web, http, response
Image: /media/pointstacker/pointstacker.png
Image_width: 1280
Image_height: 791
Summary:
    На одном из текущих проектов мы строим геоинформационную систему.
    Работаем с геоданными через [PostGIS](http://postgis.net/)
    и [GeoServer](http://geoserver.org/). Объектов на карте достаточно много
    и в перспективе будет всё больше. Отрисовка всех маркеров на крупном масштабе
    заставляет геосервер нагружать систему на 100%. Для оптимизации работы системы,
    а также повышения наглядности для пользователя. Отдельные маркеры на карте
    необходимо группировать в кластеры.

Как и положено веб фраймворку, `Django` позволяет
возвращать в ответ на запрос `HttpResponse` с любым статус кодом
из дипазона `[100 .. 599]`. Этот ответ должен быть явно отправлен
через `return` во вьюхе обрабатывающей запрос.
Однако `pythonyc way` предусматривает не только
явный `return`, но и гибкую обработку исключений.
Рассмотрим веб исключения подробнее.

### Стандартные исключения

`Django` допускает ограниченный набор `Http` ответов через
выбрасывание исключении.

- `400` [SuspiciousOperation](https://docs.djangoproject.com/en/stable/ref/exceptions/#suspiciousoperation)
- `403` [PermissionDenied](https://docs.djangoproject.com/en/stable/ref/exceptions/#permissiondenied)
- `404` [Http404](https://docs.djangoproject.com/en/stable/topics/http/views/#the-http404-exception)
- `500` Любое другое не перехваченное исключение

Каждый ответ можно настроить по вкусу через перегрузку соответсвующих
[хендлеров](https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views)

