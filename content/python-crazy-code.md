Title: Заклинатель змей?
Date: 2016-04-13 15:00
Modified: 2016-04-17 15:00
Category: Python
Tags: python, code, crazy
Image: /media/crazy-code/snake_charmer.jpg
Summary:
    `Python` имеет очень простой синтаксис, и практически всегда ведёт себя
    предсказуемо. Однако порой происходит нечто невероятное...

`Python` имеет очень простой синтаксис, и практически всегда ведёт себя
предсказуемо. Однако порой происходит нечто невероятное...

###Непредсказуемые списки

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

```Python
# list += str
x = []
x += 'abcd'
print x

# list + str
x = []
x = x + 'abcd'
print x
```

<details>
    <summary>Результат</summary>

```Python
>>> # list += str
>>> x = []
>>> x += 'abcd'
>>> print x
['a', 'b', 'c', 'd']
>>>
>>> # list + str
>>> x = []
>>> x = x + 'abcd'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate list (not "str") to list
>>> print x
[]
```

</details>

###ООП, такое ООП

```python
>>> class A():
...   def foo(self):
...     print "this is A"
... 
>>> class B():
...   def foo(self):
...     print "this is B"
... 
>>> 
>>> a = A()
>>> b = B()
>>> 
>>> a.foo()
this is A
>>> b.foob()
this is B
>>> 
>>> A.foo = B.foob
>>> 
>>> a.foo()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unbound method foob() must be called with B instance as first argument (got nothing instead)
>>> 
>>> A.foo = b.foob
>>> a.foo()
this is B
>>> 
```
