===============================
# Python pitfalls

## String operation does not work on number
Number is an integer and cannot be used alone with string operations like
join etc. Cast number to string (object) to treat it as a string.

    nums = [1, 2, 3]
    num_st = map(str, nums)
    num_st = [str(num) for num in nums]

## Comparison string number and number >, <
Very tricky !! Python does not convert string to number !! Python 3.x will
trigger exception for such comparison.

Basically, if comparison condition has string as one of operands, it will do
sort of lexical comparison where number should come before string to be true.

    if '10' < 5:
        print 'Always true since string comes after number'
    if 100 > '1000':
        print 'Always true'


=================================
# TKinter Text widget - quick getting to know

Text()
.delete,insert,set_focus,get
.image_create, window_create - embedded img, widget
.get('1.0', END)
1.0 = row 1, col 0 -> starting point

Supports system-wide clipboard
.clipboard_clear,append - TK object should have these
CLIPBOARD - also keyword for storage

Scrollbar widget (vbar)
Cannot style color and the likes since this is provide by Windows Styles

Embedd widget to Text widget
text.window_create(END, window=pbar)

Because Tkinter is single threaded, I cannot update GUI from another than main
thread, otherwise unexpected behaviour.

Cursor built-in tags to move cursor:
INSERT ('insert') - insertion cursor
CURRENT - mouse cursor position

## Tied vars in Tkinter

Updating var will update tied widget and vice versa. Useful when object is
destroyed but var still holds data.
var1 = StringVar(), IntVar()...
.config(textvariable=var1)

## Log to Tk widget

Subclass logging.Handler and override method 'emit' with own reporting
Logging module is great way to handle logging accross standard and third party
modules.
TODO READ
I shoud later study whole manual on offical python doc to get a good grasp of
all available features.

## ProgressBar from ttk

Pbar change status in GUI only when GUI is in control. When there is function
running, GUI will update pbar once the fuction has given up control.

However, it is possible to explictly ask to update GUI with these commands:
widget.update_idletask()
widget.after(MS, FUNC) where function is one-off function scheduled to run
in background no matter what is running. This still need explicit call to
make GUI to redraw (update)

Problem - explicit call to update GUI does not work when there script is running
function from different module. Even registering update_idletask with .after()
will not make GUI to redraw (and show pbar change). I've tried all I could but
found only that GUI will redraw only when function from external module
has returned. It relates to the fact that Tkitner is single thread lib.

Use threading module to create worker threads.

No, this is strange. Determinate mode animates pbar instantly but indeterminate
waits while function is running and then starts animating !!

## GUI in General

To have resposive GUI, every operation should run as a thread so
GUI remains responsive all the time. However, Tkinter GUI should not be
updated from non-main thread since Tkinter is not thread-safe and may lead to
unexpected behaviour / crash. Worker thread should communicate changes to main
thread via other mechanism like class Queue etc.

Any running function blocks GUI waiting to take over control again.

=================================
# Python design rules

Function should be a black box that gets values and returns other values,
without relying on global vars

## Singleton

It is design pattern for object that allows only one instance of an object.
First instantiation wll create object as usual. However, another call to
constructor will return reference to the first and only instance.

This can be usefull when control should be centralized to single object.
However, this technique has opponents too.

Example of singleton design

    class MySingleton(object):
        _instance = None
        def __new__(self):
            if not _instance:
                _instance = super(MySingleton).__new__(self)
            return _instance

Class Logger from logging is singleton to support global control and config.


# Module logging - best practices

Library/modules should only create logger with module name.
No configuration in terms of level etc !! This is necessary for easy
incorporation to another applications.

logger has module name to easy distinguish log's source
Another loggers in module should use format e.g '__name__.classA'
log = logging._getLogger(__name__)

No need to keep reference to a log object since it is singleton.

Additonally, use NullHandler to prevent warning message when logging is not
configured:

    import logging
    log = logging.getLogger(__name__)
    log.addHandler(logging.NullHandler())

http://pieces.openpolitics.com/2012/04/python-logging-best-practices/

## Logger level

Level is determined from logger. If not set, checks its parent, eventually
reaching root logger that has default level set to WARNING.

Logger hierarchy follows dot convention where b is child to logger a.b and a is
child to root logger

Found level then decides if message is passed to logger handler where the event
occured

Message also propagates to parent loggers - option to disable it.

logging.info() - to root logger
logger1.info() - to module-level logger (from call to .getLogger(name))

========================
# Sublime shorcuts subset

Transpose(swap) words - make at least two selections through Ctrl, then Ctrl+T

Go to anything Ctrl+P (uses fuzzy match - mpag will find mainPage)
    : line
    @ function (plus fuzzy math in other files feas@lgin to get func in ftpeasy.py

Switch project instantly (recover previously opened files/tabs) Ctrl+Atl+P
Go to line ctrl + G

## TOP SHORTCUTS
Select line Ctrl + L (press muliple times to select more lines downwards)
Open new line below Ctrl + Enter
Open new line above Ctrl + Alt + Enter
Cut and paste without indent Ctrl + X -> Ctrl + (Shift) + V

Indent line Ctrl + [ or ]  , for block selection Ctrl + (Shift) + Tab
Comment line Ctrl + /

Quick movement
move line ctrl + shift + up/down (no need to highlight)
move among words ctrl + left/right arrow
Move keys added - ctrl + i, j, k, l

Delete word ctrl + backspace/delete

Slurp find string ctrl + E (highlight all strings matching the one under
cursor), use f3 and shift + f3 to move between occurences

Less mouse, better productivity

=============================
# Python - object oriented

__name__ inside class gives still name of module, NOT the name of class

## Data encapsulation

When creating class, think about attributes:
- users need to access it, make it public self.x
- users should not access it - make it private self.__x
- you need to run some checks on attribute, use property decorator without
the need to change interface

Do NOT use explicit getter or setter funcs but be Pythonic and use property

    self.x = x

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        if val < 0:
            val = 0
        self.__x = vav

    myObj.x
    myObj.x = -10

Attribute types
- public
- protected _x: it should be used only when subclassed or at your own risk
- private __x: invisible and inaccessible from outside the class

Switch statement (or cascaded if-else)
Pythonic way is to use hash table - much better and elegant

====================
# Programming best practices

## Always initialize from data
Meaning to init function vars from data given rather than building own
arbitrary data

## TDD
**Very interesting concept that may use python's assert.**

At least, I should write few test for each black box - function etc. !!

This idea building tests beforehand helps to prevent issues of missed edge
cases. It also nicely documents function API and its correct use. Not to
mention possibility of running unit tests to ensure no regression.

http://swcarpentry.github.io/python-novice-inflammation/08-defensive.html

def test_range_overlap():
    assert range_overlap([ (0.0, 1.0), (5.0, 6.0) ]) == None
    assert range_overlap([ (0.0, 1.0), (1.0, 2.0) ]) == None
    assert range_overlap([ (0.0, 1.0) ]) == (0.0, 1.0)
    assert range_overlap([ (2.0, 3.0), (2.0, 4.0) ]) == (2.0, 3.0)
    assert range_overlap([ (0.0, 1.0), (0.0, 2.0), (-1.0, 1.0) ]) == (0.0, 1.0)

## Python Syntax

Function parameters will become local variable

Enclosing scope - inner function has access to variables in outer function, at
least read and sometimes modify access

## Python auto-complete
Autocomplete works fine for object created directly from class. However, it
will not work when object instance is created by a method call. This is a
disadvantage of dynamically linked langs. It would be too difficult for IDE to
figure out what is the class of a instance object.

This issue is present on all editors as far as I know - Sublime, PyCharm, PyDev
in Eclipse.

However, it will work fine when you tell IDE what kind of class is the object.

1. Find object's class
    obj.__class__ , or type(obj).__class__.__name__

2. Tell IDE
    assert isinstance(obj, 'className')

3. Next line after assert should give all suggestions

========================================
# BeautifulSoup

.next_elements
will walk through all elements sequencially including nested too

parsers
- html.parser is not a good one since it does not handle nicely self-closed
elements
- lxml parser is best from supported

