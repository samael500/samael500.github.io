Title: Кластеризация маркеров в GeoServer
Date: 2017-05-10 15:00
Modified: 2017-05-10 15:00
Category: Python
Tags: geoserver, map, postgis, gis, geodata
Image: /media/aiochat/aiochat.png
Image_width: 1280
Image_height: 791
Summary:


На одном из текущих проектов мы строим геоинформационную систему.
Работаем с геоданными через [PostGIS](http://postgis.net/)
и [GeoServer](http://geoserver.org/). Объектов на карте достаточно много
и в перспективе будет всё больше. Отрисовка всех маркеров на крупном масштабе
заставляет геосервер нагружать систему на 100%. Для оптимизации работы системы,
а так же -- повышения наглядности для пользователя. Отдельные маркеры на карте
необходимо группировать в кластеры.

Как оказалось, сделать это силами геосервара очень просто,
но пока этот способ был найден, прешлось перерыть
всю документацию по геосерверу и весь `Gis StackExchange`. В результате
группировка точек в кластеры делается с помощью векторной трансформации
[vec:PointStacker](http://docs.geoserver.org/latest/en/user/styling/ysld/reference/transforms.html#point-stacker).

### Группировка точек

```xml
<Transformation>
    <ogc:Function name="vec:PointStacker">
        <ogc:Function name="parameter">
            <ogc:Literal>data</ogc:Literal>
        </ogc:Function>
        <ogc:Function name="parameter">
            <ogc:Literal>cellSize</ogc:Literal>
            <ogc:Literal>99</ogc:Literal>
        </ogc:Function>
        <ogc:Function name="parameter">
            <ogc:Literal>outputBBOX</ogc:Literal>
            <ogc:Function name="env">
                <ogc:Literal>wms_bbox</ogc:Literal>
            </ogc:Function>
        </ogc:Function>
        <ogc:Function name="parameter">
            <ogc:Literal>outputWidth</ogc:Literal>
            <ogc:Function name="env">
                <ogc:Literal>wms_width</ogc:Literal>
            </ogc:Function>
        </ogc:Function>
        <ogc:Function name="parameter">
            <ogc:Literal>outputHeight</ogc:Literal>
            <ogc:Function name="env">
                <ogc:Literal>wms_height</ogc:Literal>
            </ogc:Function>
        </ogc:Function>
    </ogc:Function>
</Transformation>
```
