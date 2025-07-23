# 1
a, *b = "abcd"
print(a, b)
# >>> a ['b', 'c', 'd']
# Распаковка последовательности с использованием *


# 2
a = "abcd"
a[0] = "e"
# >>> TypeError: 'str' object does not support item assignment
# Строки неизменяемы, поэтому выведет ошибку


# 3
print(all([0, 1]))
print(all([]))
print(any([]))
# >>> False (не все элементы истинны)
# >>> True (элементов нет => ни один не ложный)
# >>> False (нет ни одного истинного элемента)


# 4
class Foo:
    def __getitem__(self, item):
        return item

f = Foo()
print(next(iter(f)))
# >>> 0
# __getitem__() позволяет эмулировать итератор, затем next() вызывает f[0]


# 5
class Foo:
    def __getitem__(self, item):
        return item

for i in Foo():
    print(i)
# >>> бесконечный цикл


# 6
def foo(a, /, *, b):
    pass

foo("a", "b")
# >>> TypeError: foo() takes 1 positional argument but 2 were given
# b передается позиционно


# 7
def func(x, nums=[]):
    nums.append(x)
    return nums

print(func(1))
print(func(2))
# >>> [1]
# >>> [1, 2]
# nums ссылается на один и тот же объект в памяти, сохраняемый между вызовами


# 8
def foo():
    for num in range(1, 10):
        yield num

f = foo()

for i in iter(lambda: next(f), 5):
    print(i)
# >>> 1
# >>> 2
# >>> 3
# >>> 4
# sentinel=5 => итератор останавливается


# 9
a = [10, 11, [20, 21]]
b = a.copy()
b[2][0] = 10

print(a)
# >>> [10, 11, [10, 21]]
# .copy() - поверхностная копия, a[2] и b[2] - один и тот же вложенный список


# 10
def foo(x):
    yield 1
    yield 2
    return x

f = foo(3)
print(next(f))
print(next(f))
print(next(f))
# >>> 1
# >>> 2
# >>> StopIteration: 3
# Генератор встречает return и возбуждает исключение со значением 3


# 11
1 < 2 < 3 < 1 or print("hi")
# >>> hi
# Условие слева неверное


# 12
x = 10

def foo1():
    print(x)

def foo2():
    print(x)
    x = 20

foo1()
foo2()
# >>> UnboundLocalError: cannot access local variable 'x' where it is not associated with a value
# >>> 10
# В foo2 присутствует операция локального присваивания, после печати глобальной переменной


# 13
a = [[]] * 3
a[0].append(1)
print(a)
# >>> [[1], [1], [1]]
# Список из трех ссылок, ссылающихся на один и тот же объект


# 14
a = "abc" * 3
b = "abcabcabc"
print(a == b)
print(a is b)
# >>> True
# >>> True
# Интернирование строк


# 15
a = []
b = []
print(a == b)
print(a is b)
# >>> True (одинаковое содержимое)
# >>> False (разные объекты в памяти)

a = ()
b = ()
print(a == b)
print(a is b)
# >>> True (одинаковое содержимое)
# >>> True (интернирование кортежей)

a = (1, 2, 3)
b = (1, 2, 3)
print(a is b)
# в интерпретаторе:
# >>> True (интернирование небольшого неизменяемого объекта)
# как скрипт:
# >>> False (не интернируется)


# 16
a = sum([True, False, True, False, True])
print(a)
# >>> 3
# Логические значения - подкласс int


# 17
a = [1, 2]
b = a
a = a + [3]
a.append(4)
print(b)
# >>> [1, 2]
# b ссылается на оригинальный список


# 18
class A:
    x = 1

class B(A):
    pass

class C(A):
    pass

B.x = 2
A.x = 3

print(B.x, C.x)
# >>> 2 3
# Переопределение атрибута родительского класса происходит между присваиваниями значений атрибутам дочерних


# 19
import random


class Foo:
    def __init__(self, x):
        self.x = x

    def __hash__(self):
        return hash(random.randint(0, self.x))


f = Foo(1)
a = {f: "value"}
print(a.get(f))
print(a.get(f))
print(a.get(f))
# >>> None / value
# >>> None / value
# >>> None / value
# Нарушается ключевое требование для dict - хэш-значение одного и того же объекта не должно меняться


# 20
a = 256
b = 256
print(a is b)
# >>> True

a = 257
b = 257
print(a is b)
# в интерпретаторе:
# >>> True
# как скрипт:
# False (интернируются числа в диапазоне [-5, 256])


# 21
def foo1():
    global a
    a = 1

foo1()
print(a)

def foo2():
    global b
    b = 1

print(b)
foo2()
# >>> NameError: name 'b' is not defined
# >>> 1
# Попытка вызвать глобальную переменную b до вызова функции


# 22
def foo():
    a = []

    def bar(b):
        a.append(b)
        return a

    return bar

f = foo()
print(f(1))
print(f(2))
print(f(3))
print(f.__closure__[len(f.__closure__) - 1].cell_contents)
# >>> [1]
# >>> [1, 2]
# >>> [1, 2, 3]
# >>> [1, 2, 3]
# f - функция bar в замкнутом состоянии => список a сохраняется между вызовами
# f.__closure__ — это кортеж ячеек, в которых хранятся закрытые переменные


# 23
class Creature:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        print(f"__getattr__({attr})")
        return self.name if attr != "fly" else None

    def __getattribute__(self, item):
        print(f"__getattribute__({item})")
        return super().__getattribute__(item) if item != "sound" else "sound"


class Animal(Creature):
    def verbose(self):
        return self.name


class Bird(Animal):
    pass


bird = Bird("кеша")

print("\nbird.name: ")
print(bird.name)
# >>> bird.name:
# >>> __getattribute__(name)
# >>> кеша
print("\nbird.verbose: ")
print(bird.verbose)
# >>> bird.verbose:
# >>> __getattribute__(verbose)
# >>> <bound method Animal.verbose of <__main__.Bird object at 0x00000141D29D4FD0>>
print("\nbird.sound: ")
print(bird.sound)
# >>> bird.sound:
# >>> __getattribute__(sound)
# >>> sound
print("\nbird.fly: ")
print(bird.fly)
# >>> bird.fly:
# >>> __getattribute__(fly)
# >>> __getattr__(fly)
# >>> None


# 24
def apply(value):
    match value:
        case str() if len(value.split()) == 2:
            a, b = value.split()
            print(a, b)
        case {"a": a, "b": b}:
            print(a, b)
        case [a, b]:
            pass
        case _:
            pass
    print("PRINT", a, b)


apply("a b")
apply({"a": "A", "b": "B", "c": "C"})
apply(["I", "J"])
apply(["I", "J", "K"])
# >>> a b
# >>> PRINT a b
# >>> A B
# >>> PRINT A B
# >>> PRINT I J
# >>> UnboundLocalError: cannot access local variable 'a' where it is not associated with a value