Title: Кластеризация маркеров в GeoServer
Date: 2017-05-10 15:00
Modified: 2017-05-10 15:00
Category: Python
Tags: geoserver, map, postgis, gis, geodata, sld
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

<link rel="stylesheet" href="/extra/wbt/comparator.css">
<script src="/extra/wbt/comparator.js"></script>

### Кластеризация точек

Для объединения объектов в один кластер, необходимо в стиле слоя объявить
векторную трансформацию `vec:PointStacker`.

Данная трансформация принимает следующие параметры:

- `cellSize` -- Размер ячейки в пределах которой точки будут объединятся в кластер.
- `outputBBOX` -- Координаты углов результирующего тайла.
- `outputWidth` -- Ширина результирующего тайла.
- `outputHeight` -- Высота результирующего тайла.

На выходе получаем кластеры с информацие о количестве объектов.

- `geom` -- геометрия кластера.
- `count` -- число объектов вошедших в кластер.
- `countUnique` -- число уникальных объектов в кластере.

Размер ячейки выбираем "на глаз", что бы объекты красиво группировались
с точки зрения пользователя. Чем больше ячейка, тем меньше кластеров
получается в результате.

Остальные параметры передаем из исходного тайла через функцию `env`
входящего `wms` запроса.

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

Далее для кластеров необходимо задать стиль отображения. Будем рисовать
кластеры кругами с надписыванием количества объектов. Размер круга выбираем
в зависимости от числа объектов вошедших в него, например по формуле:

```python
25 + log (count) / 5
```

Стиль состоит из описания текста `TextSymbolizer` и точки `PointSymbolizer`.

```xml
<Rule>
    <Name>Point group cluster</Name>
    <Title>Realties group</Title>
    <TextSymbolizer>
        <Label>
            <ogc:PropertyName>count</ogc:PropertyName>
        </Label>
        <Font>
            <CssParameter name="font-family">Arial</CssParameter>
            <CssParameter name="font-size">12</CssParameter>
            <CssParameter name="font-weight">bold</CssParameter>
        </Font>
        <LabelPlacement>
            <PointPlacement>
                <AnchorPoint>
                    <AnchorPointX>0.5</AnchorPointX>
                    <AnchorPointY>0.8</AnchorPointY>
                </AnchorPoint>
            </PointPlacement>
        </LabelPlacement>
        <Fill>
            <CssParameter name="fill">#000</CssParameter>
            <CssParameter name="fill-opacity">1.0</CssParameter>
        </Fill>
        <VendorOption name="partials">true</VendorOption>
    </TextSymbolizer>
    <PointSymbolizer>
        <Graphic>
            <Mark>
                <WellKnownName>circle</WellKnownName>
                <Fill>
                    <CssParameter name="fill">#1E90FF</CssParameter>
                    <CssParameter name="fill-opacity">0.75</CssParameter>
                </Fill>
            </Mark>
            <Size>
                <ogc:Add>
                    <ogc:Literal>25</ogc:Literal>
                    <ogc:Mul>
                        <ogc:Function name="log">
                           <ogc:PropertyName>count</ogc:PropertyName>
                        </ogc:Function>
                        <ogc:Literal>5</ogc:Literal>
                    </ogc:Mul>
                </ogc:Add>
            </Size>
        </Graphic>
    </PointSymbolizer>
</Rule>
```

В одном слое у нас отображаются объекты разных торговых сетей,
и стиль иконок должен быть различным для них.
Но при кластеризации сохраняется только информация о количестве объектов,
но никак не о качестве. Даже для кластера из одного объекта.
Поэтому будем запускать кластеризацию начиная с некоторого масштаба.
А для меньшего масштаба отображать все точки отдельно.

Разделить отображения можно с помощью задания минимального
и максимального масштаба отображения.

```xml
<!-- Стиль отдельного объекта -->
<MaxScaleDenominator>70000</MaxScaleDenominator>

<!-- Стиль кластера -->
<MinScaleDenominator>70000</MinScaleDenominator>
```

### Результат

<details>
    <summary>Весь стиль объектов</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
    <NamedLayer>
        <Name>Realties</Name>
        <UserStyle>
            <Name>Realties</Name>
            <Title>Realties objects icons</Title>
            <Abstract>SVG styles for realties objects</Abstract>

            <FeatureTypeStyle>
                <Rule>
                    <MaxScaleDenominator>70000</MaxScaleDenominator>
                    <Title>Realty</Title>
                    <PointSymbolizer>
                        <Graphic>
                            <ExternalGraphic>
                                <OnlineResource
                                    xlink:type="simple"
                                    xlink:href="./img/${logo_name}.svg" />
                                <Format>image/svg+xml</Format>
                            </ExternalGraphic>
                            <Size>
                                <ogc:Literal>35</ogc:Literal>
                            </Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
            </FeatureTypeStyle>

            <FeatureTypeStyle>
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

                <Rule>
                    <MinScaleDenominator>70000</MinScaleDenominator>
                    <Name>Point group cluster</Name>
                    <Title>Realties group</Title>
                    <TextSymbolizer>
                        <Label>
                            <ogc:PropertyName>count</ogc:PropertyName>
                        </Label>
                        <Font>
                            <CssParameter name="font-family">Arial</CssParameter>
                            <CssParameter name="font-size">12</CssParameter>
                            <CssParameter name="font-weight">bold</CssParameter>
                        </Font>
                        <LabelPlacement>
                            <PointPlacement>
                                <AnchorPoint>
                                    <AnchorPointX>0.5</AnchorPointX>
                                    <AnchorPointY>0.8</AnchorPointY>
                                </AnchorPoint>
                            </PointPlacement>
                        </LabelPlacement>
                        <Fill>
                            <CssParameter name="fill">#000</CssParameter>
                            <CssParameter name="fill-opacity">1.0</CssParameter>
                        </Fill>
                        <VendorOption name="partials">true</VendorOption>
                    </TextSymbolizer>
                    <PointSymbolizer>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#1E90FF</CssParameter>
                                    <CssParameter name="fill-opacity">0.75</CssParameter>
                                </Fill>
                            </Mark>
                            <Size>
                                <ogc:Add>
                                    <ogc:Literal>25</ogc:Literal>
                                    <ogc:Mul>
                                        <ogc:Function name="log">
                                           <ogc:PropertyName>count</ogc:PropertyName>
                                        </ogc:Function>
                                        <ogc:Literal>5</ogc:Literal>
                                    </ogc:Mul>
                                </ogc:Add>
                            </Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
            </FeatureTypeStyle>

        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>
```

</details>


Для сравнения представлены изображения с кластеризацией объектов и без неё.

<div id='map'></div>

<div id='map-zoom'></div>

Так же, кластеризация позволила значительно увеличить производительность системы.
Рендер большого числа отдельных маркеров выполнялся медленно и существенно
нагружал процессор. Часто соединение обрывалось по `504`.
Объединение в кластеры работает очень быстро без нагрузки на систему.

Кластеризованый результат (полная карта) загружается в среднем за 1.6 секунд.
Тогда как отдельные маркеры грузились порядка 130 секунд.

#### Загрузка кластеризированных маркеров

![waterfall cluster](/media/pointstacker/waterfall-cluster.png){.center}

Load Time | First Byte | Start Render | Speed Index | Interactive (beta) | Time | Requests | Bytes In
--------- | ---------- | ------------ | ----------- | ------------------ | ---- | -------- | --------
  1.697s  |   1.669s   |     3.780s   |     3780    |       > 3.813s     |1.697s|     1    |   9 KB

#### Загрузка отдельных маркеров

![waterfall points](/media/pointstacker/waterfall-points.png)

Load Time | First Byte | Start Render | Speed Index | Interactive (beta) | Time | Requests | Bytes In
--------- | ---------- | ------------ | ----------- | ------------------ | ---- | -------- | --------
 130.397s |   8.268s   |    21.934s   |     57691   |        8.445s      |130.397s |  1    | 960 KB

<script>
$("#map").wbtComparator({
    // direction: "horizontal",
    src: ["/media/pointstacker/cluster.png", "/media/pointstacker/objects.png"],
    timeout: false
});
$("#map-zoom").wbtComparator({
    // direction: "horizontal",
    src: ["/media/pointstacker/zoom-cluster.png", "/media/pointstacker/zoom-objects.png"],
    timeout: false
});
$('table').addClass('table table-bordered table-responsive');
</script>
