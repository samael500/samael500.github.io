Title: Автосодержание в Pelican
Date: 2015-09-02 15:00
Modified: 2015-09-02 15:00
Category: Другое
Tags: python, pelican, markdown, md, autonav, anchor, javascript, css
Summary:
    Так получается, что некоторые статьи, например
    [ралли на браузерах](|filename|/python-browsers.md). Содержат в себе несколько
    уровней заголовков. И в связи с этим, хотелось сделать автоматическую навигацию
    по статье.

Так получается, что некоторые статьи, например
[ралли на браузерах](|filename|/python-browsers.md). Содержат в себе несколько
уровней заголовков. И в связи с этим, хотелось сделать автоматическую навигацию
по статье.

##Якоря в заголовках markdown

Для написания постов блога я использую 
[markdown](http://daringfireball.net/projects/markdown/) разметку текста.
Для того, чтобы при генерации `html` заголовкам присваивались якоря - необходимо
подключить расширение
[Table of Contents](https://pythonhosted.org/Markdown/extensions/toc.html).
Делается это элементарно прописав в `pelicanconf.py` следующую строчку:

```python
MD_EXTENSIONS = [
    'codehilite(css_class=highlight)', 'extra', 'markdown.extensions.toc' ]
```

Теперь при генерации `html` каждому заголовку будет присваиваться `id`
содержащимся текстом. Заголовок:

```Markdown
##Markdown anchors
```

Будет сгенерирован в такой `html`:

```html
<h2 id="markdown-anchors">Markdown&nbsp;anchors</h2>
```

###Ссылки в заголовках

Чтобы заголовки были непросто тегами `h1` ... `h6`, а содержали ссылку на
самих себя нужно добавить аргумент `anchorlink`. Теперь конфигурация
`MD_EXTENSIONS` выглядит так:

```python
MD_EXTENSIONS = [
    'codehilite(css_class=highlight)', 'extra',
    'markdown.extensions.toc(anchorlink=True)' ]
```

Заголовок:

```Markdown
##Markdown anchors
```

Будет сгенерирован в такой `html`:

```html
<h2 id="markdown-anchors">
    <a class="toclink" href="#markdown-anchors">Markdown&nbsp;anchors</a>
</h2>
```

###Кириллица в заголовках

К сожалению, стандартный `slugify` который используется в `markdown toc` не
умеет обрабатывать кириллические символы, и поэтому заголовок.

```Markdown
##Ссылка в заголовке
```

Будет сгенерирован в такой `html`:

```html
<h2 id="_1">
    <a class="toclink" href="#_1">Ссылка в&nbsp;заголовке</a>
</h2>
```

Что бы исправить это, можно воспользоваться библиотекой
[python slugify](https://pypi.python.org/pypi/python-slugify), задав
`TocExtension` объект `slugify`. Объект `slugify` должен быть `callable`
поэтому не обойтись просто строковым указанием аргументов, придется явно
импортировать и указывать в конструкторе аргументы для расширения:

```python
from markdown.extensions.toc import TocExtension
from slugify import slugify
MD_EXTENSIONS = [
    'codehilite(css_class=highlight)', 'extra',
    TocExtension(anchorlink=True, slugify=slugify), ]
```

##Меню автосодержания

Для навигации по заголовкам будем использовать `jQuery plugin`
[Anchorific.js](http://renaysha.me/anchorific-js/). Данный плагин умеет
самостоятельно присваивать `id` заголовкам, но поскольку заголовки уже
сгенерированы с якорями, то создание ссылок джаваскриптом использоваться
не будет, в конструкторе укажем `null` значения для текста и позиции ссылки
в заголовке.

```javascript
    $('article.content').anchorific({
        anchorClass: null, anchorText: null, spy: true, position: null, anchor: null,
    });
```

Так же пришлось немного подправить напильником этот плагин, под конкретные задачи,
например заставить его искать не все заголовки, а только с идентификаторами.

```diff
- self.headers = self.$elem.find( 'h1, h2, h3, h4, h5, h6' );
+ self.headers = self.$elem.find( 'h1[id], h2[id], h3[id], h4[id], h5[id], h6[id]' );
```

###"Липучее" меню

Для того, что бы при скролинге страницы меню навигации всегда оставалось
доступным будем использовать `position: fixed;`, но присваивать его только
при достижении вершины объекта при скролинге.

Создадим класс `sticky` и будем навешивать его по событию скрол.

```css
.sticky {
    position: fixed;
    top: 33px;
    z-index: 999;
}
```

```javascript
var $window = $(window),
    $sticky = $('div.anchorific'),
    sticky_top = $sticky.offset().top;

$window.scroll(function() {
    $sticky.toggleClass('sticky', $window.scrollTop() > sticky_top - 33);
});
```

Получилось такое автосодержание:

![nav](/media/md-headers/nav.png){.center}
