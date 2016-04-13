Title: Как прострелить себе ногу? Или что делает этот код?
Date: 2016-04-13 15:00
Modified: 2016-04-13 15:00
Category: Python
Tags: python, code, crazy
Image: 
Summary:
    `Python` имеет очень простой синтаксис, и практически всегда ведёт себя
    предсказуемо. Однако порой происходит нечто невероятное...

`Python` имеет очень простой синтаксис, и практически всегда ведёт себя
предсказуемо. Однако порой происходит нечто невероятное...

```Python
x = [[]] * 3
x[0].append('a')
x[1].append('b')
x[2].append('c')
x[0] = ['d']
print x
```

<details>
    <summary>Результат</summary>

```Python
>>> x = [[]] * 3
>>> x[0].append('a')
>>> x[1].append('b')
>>> x[2].append('c')
>>> x[0] = ['d']
>>> print x
[['d'], ['a', 'b', 'c'], ['a', 'b', 'c']]
```

</details>

```Python
a = ([], )
a[0].extend([1])
a[0] += [2]
print a[0]
```

<details>
    <summary>Результат</summary>

```Python
>>> a = ([], )
>>> a[0].extend([1])
>>> a[0] += [2]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> print a[0]
[1, 2]
```

</details>
