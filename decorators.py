"""
26.9.2105

DECORATOR - DESIGN PATTERN

The simplest decorator form:

def decor(func):
    def wrapper(*args):
        return 'extra stuff, {0}'.format(func(*args))
    return wrapper

def do_stuff():
    print 'doing stuff'

do_stuff = decor(do_stuff)
do_stuff()

# Decorater's goal
To decorate (change) function's ouput without modifying function's body.


# Decorator facts
Decorator will return function reference that will replace original
(undecorated) function. Let's call this *decorated function*.

*Decorated function* is in essence a function wrapper in the body of decorater.
This wrapper will wrap around original function so it can alter function output
when the decorated function is called (aka postponed execution).

Because decorater's wrapper is in fact decorated function, it should accept
and pass along any arguments for original function.


# Decorater is a closure
This fact is not essential for understanding decorators. It is rather look
behind the scene. First off, let's explain following terms.

## Enclosing scope
When a function is nested in another function, the inner function has access to
outer's function variables unless local variables shadows them. This is
*enclosing scope* for the inner function. As a side note, inner function has
only read access to mutable variables in outer function.

## Closure (aka a factory function)
It is a function reference that remembers variables from enclosing scope. In
other words, the closure has access to enclosing scope (outer variables) even
after the outer function has finished execution and its variables should
normally go out of scope and be garbage-collected.

Now, decorater in its simplest form is a closure because it returns function
reference that remembers variable holding original function (object) while the
variable went out of scope.

Here, *func* holds original function as an object. When the *wrapper* is called
later to stand in original function, it is obvious that *func* is out of scope
at this moment.

def decor(func):
    def wrapper(*args):
        return func(*args)
    return wrapper


# Conclusion
I still do not know how to take advantage of *decorators* but it is apparently
big thing remotely similar to discovery of OO.
AFAIK, python's famous frameworks heavily relies on decorators as Twisted and
Flask.

[Source 1](http://thecodeship.com/patterns/guide-to-python-function-decorators/)
[Source 2](http://www.python-academy.com/download/ep14deco/iter_gen_dec_handout.pdf)
[Cheatsheet](http://www.pydanny.com/python-decorator-cheatsheet.html)
"""

def new_car(model):
    return 'your new ' + model

print new_car('Nissan GTR')

def bodywork_decorator(car_func):
    # define nested function and return reference (it does not run here)
    # nested function will require args necessary for fuction to be decorated
    def bodywork(model):
        return 'Blue rimms, carbon hood on {0}'.format(car_func(model))
    return bodywork

# first working hand-made decorator
new_car_ng = bodywork_decorator(new_car)
print new_car_ng('Ferrari Italia')

# python shortcut with @
@bodywork_decorator
def new_car_pythonic(model):
    return 'your new ' + model
print new_car_pythonic('Octavia')

# stack decorators
def engine_decorator(car_func):
    def decorate(model):
        return '{0} with V8 engine'.format(car_func(model))
    return decorate

@engine_decorator
@bodywork_decorator
def new_car_again(model):
    return 'your new ' + model
print new_car_again('Volvo')

# in OO
# Accomodate for 'self' reference passed to object's method by *args
def engine_decorator(car_func):
    def decorate(*args, **kwargs):
        # decorated function can now accept any number of args
        return '{0} with V8 engine'.format(car_func(*args, **kwargs))
    return decorate

class NewCar(object):
    def __init__(self, model):
        self.model = model
    @engine_decorator
    def __str__(self):
        return 'your new ' + self.model
new_car = NewCar('Honda')
print new_car

# decorator that accepts arg(s)
# - args passed when decorated function is called
def paint(color, shade):
    def wrapper1(car_func):
        def wrapper2(model):
            return '{0} in {1} {2}'.format(car_func(model), color, shade)
        return wrapper2
    return wrapper1

@paint('blue', 'metalic')
def new_car(model):
    return 'your brand new ' + model
print new_car('Dacia')

# decorator will unfortunately change some function attributes as a result of
# replacing original function, to fix those, use functools.wraps
from functools import wraps

def bodywork_decorator(car_func):
    @wraps(car_func)
    def bodywork(model):
        return 'Blue rimms, carbon hood on {0}'.format(car_func(model))
    return bodywork

@bodywork_decorator
def new_car(model):
    "Show new car"
    return 'your brand new ' + model
# print new_car('Dacia')
print 'name: %s, doc: %s' % (new_car.__name__, new_car.__doc__)


exit()

# Closure
# It is closure only and only if variable is gotten from enclosing scope

# Function closure is feature that allows function defined in non-global space
# to remeber enclosing namespace 'at definition time'
def a():
    x = 10
    def b():
        # 'x' comes from enclosing scope, not from function 'b' args
        print x + 2
    return b
c = a()
# show None for non-closure function ref
print c, c(), c.func_closure

# this closure requires x available at runtime of func 'a'
# funtion's args will become local vars and thus will be in enclosing scope
def a(x):
    def b():
        print x + 5
    return b
cc = a(-2)
print cc(), cc.__closure__
