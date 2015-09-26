"""Code snippets, reference and design patterns

Note - it is not supposed to run as a script !
"""

import time
import threading
import Tkinter
import ttk

# Simple threading example
def do_work():
    print 'start work'
    time.sleep(5)
    print 'work done'

worker = threading.Thread(target=do_work)
worker.start()
while worker.is_alive():
    # notice race condition when thread and while loop attempts to write string
    print 'thread is running'
    time.sleep(2)

# Tkinter, TK
class ThreadClient(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        print 'sleep now'
        time.sleep(5)
        print 'sleep over'

class TestGui(Frame):
    def __init__(self, parent=None, *args):
        Frame.__init__(self, parent, *args)
        self.pack()
        self.make_widgets()
        self.mainloop()

    def make_widgets(self):
        btn = Button(self, text='Run test', command=self.run_test)
        te = Text(self, width=10, height=10)
        te.insert(END, 'text box 1')
        pbar = ttk.Progressbar(self, mode='indeterminate')

        btn.pack()
        te.pack()
        pbar.pack()

        self.btn = btn
        self.te = te
        self.pbar = pbar

    def refresh_pbar(self):
        self.pbar.step(10)
        self.pbar.update_idletasks()
        self.pbar.after(10, self.refresh_pbar)

    def run_test(self):
        self.thread = ThreadClient(queue=None)
        self.thread.start()
        self.pbar.start()

def relief_types():
    styles = ['flat', 'groove', 'raised', 'ridge', 'solid', 'sunken']
    root = Tk()
    for style in styles:
        Label(root, text=style, font=('Verdana', 20), bg='blue', bd=15,
              relief=style).pack()
    root.mainloop()

# OO
# data encapsulation - decorator property
class Foo(object):
    def __init__(self, arg):
        self.arg = arg

    @property
    def arg(self):
        return self.__arg

    @arg.setter
    def arg(self, val):
        if val is None:
            val = 'empty'
        self.__arg = val

bob = Foo('abc')
print bob.arg
bob.arg = None
print bob.arg
