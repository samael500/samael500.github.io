Title: Чистый код -- меньше забот
Date: 2017-07-10 15:00
Modified: 2017-07-10 15:00
Category: Python
Tags: code, style, pep8, codestandart
Image: /media/ /web-exceptions.png
Image_width: 1280
Image_height: 791
Summary:

<!-- Сопровождение, обновление и внесение нового функционала в `legacy` код --  -->

### Табы или пробелы?

Безусловно пробелы. Недавно на `stackoverflow` собрали
[статистику](https://stackoverflow.blog/2017/06/15/developers-use-spaces-make-money-use-tabs/)
и определили что пробелы всреднм приносят больший заработок чем табуляция.
Но это конечно же шуточный аргумент, если серьезно, ответ гораздо проще.
Иногда нужно отредактировать код по `ssh` на удаленной машине, иногда нужно
взглянуть на код в `web` интерфейсе системы контроля версий,
иногда приходится открывать код в другом редакторе.
Код должен всегда выглядеть одинаково независимо от настроек системы,
это гарантируют проблеы, но не обещает табуляция.

Один и тот же фрагмент кода, с использованием пробелов и табуляции может
выглядить очень по разному, что может приводить к ошибкам при редактировании.
Особенно это опасно в `python`, т.к. в этом случае можно перепутать уровень
вложенности и нарушить логику программы.

```python
class Foo(object):

    """ some Foo class """

    def bar(self, *args, **kwargs):
        for i in range(42):
            yield i
```

Этот код будет очень по разному выглядить в разных редакторах.

![nano tabs](/media/clean-code/nano-tabs.png){.center}
![vim tabs](/media/clean-code/vim-tabs.png){.center}
![sublime tabs](/media/clean-code/sublime-tabs.png){.center}

```diff
diff --git a/example.py b/example.py
index 8ed55ea..f88b207 100644
--- a/example.py  # tabs
+++ b/example.py  # spaces
@@ -1,7 +1,7 @@
 class Foo(object):
 
-       """ some Foo class """
+    """ some Foo class """
 
-       def bar(self, *args, **kwargs):
-               for i in range(42):
-                       yield i
+    def bar(self, *args, **kwargs):
+        for i in range(42):
+            yield i
```

Иногда табуляция может иметь ширину 0, но тем неменее присутсвовать в отступах в коде.

![tab width](/media/clean-code/tabwidth.png){.center}

