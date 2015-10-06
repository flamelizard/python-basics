"""Internet browser in python

Support subset of html markup nad simple rendering

App Spec in progress
simple GUI
donwload web page
display text elements in GUI

Improvements
Thread long running task to not block gui main loop
Text screen scrollbar

Branch code
"""

"""Learnt

# Tkinter

Cursor built-in tags to move cursor:
INSERT ('insert') - insertion cursor
CURRENT - mouse cursor position

.mark_set()

"""

from Tkinter import *
import threading
import time
import urllib2
import bs4
import re

class Browser(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack(expand=YES, fill=BOTH)
        self.home_addr = 'localhost/d:/git-repos/test_site/index.html'
        self.elem_style = {
            'h1': ('Verdana', 20, 'bold'),
            'h2': ('Arial', 15, 'bold'),
            'p': ('Verdana', 12),
            'small': ('Verdana', 10),
            'em': ('Verdana', 10, 'italic')
        }
        self.font_def = ('Verdana', 15)
        self.make_widgets()
        self.mainloop()

    def fetch_addr(self, event):
        """Fetch str from address bar"""
        # print type(event), dir(event), dir(event.widget)
        widget = event.widget
        addr = widget.get('1.0', END)
        addr = addr.strip()
        print 'fetch addr: ', addr
        self.write_addr(addr)
        self.handle_request(addr)

    def write_addr(self, addr):
        # reset cursor position, emulate browser behaviour
        widget = self.addr_bar

        widget.delete('1.0', END)
        widget.insert(1.0, addr)
        widget.mark_set(INSERT, '1.0')
        # widget.mark_gravity(INSERT, LEFT)
        # print widget.index(INSERT)

    def make_widgets(self):
        self.addr_bar = Text(self)
        # self.ca = Canvas(self)
        self.screen = Text(self)

        self.addr_bar.config(width=70, height=1, padx=5, pady=1, bd=2)
        self.addr_bar.bind('<Return>', self.fetch_addr)
        self.addr_bar.insert('1.0', self.home_addr)
        # self.ca.config(bd=2, bg='light steel blue')
        # self.ca.create_text(100, 50, text='ABCEFG', font=('Arial', 20))
        self.screen.config(height=30, bg='light steel blue')
        self.screen.config(state=DISABLED)

        self.addr_bar.pack(fill=X)
        self.add_bookmark_bar()
        # self.ca.pack(expand=YES, fill=BOTH)
        self.screen.pack(expand=YES, fill=BOTH)

    def add_bookmark_bar(self):
        home = 'www.centrum.cz'
        bar = Frame(self)
        bar.pack(expand=YES, fill=X)
        btn1 = Button(bar, text='Home', command=lambda: self.write_addr(home))
        btn1.pack(side=LEFT)

    def handle_request(self, addr):
        # worker = threading.Thread(target=lambda: self.get_page(addr))
        # # worker must put any value to self.queue to call out finish
        # worker.start()
        self.get_page(addr)

    def get_page(self, addr):
        # time.sleep(10)
        pref = 'file://' if addr.find('localhost') != -1 else 'http://'
        url = pref + addr
        reply = urllib2.urlopen(url)
        html = reply.read()
        print url, reply

        on_display = []
        soup = bs4.BeautifulSoup(html, 'html.parser')
        soup.prettify()

        text_elems = ['h1', 'h2', 'p', 'small', 'em']
        for elem in soup.body.next_elements:
            if elem.name in text_elems:
                if elem.string:
                    text = (elem.string, elem.name)
                    print text
                    on_display.append(text)
            if elem.name == 'span':
                try:
                    attr = elem['class']
                    if attr[0] == 'text':   # attribute's values is in the list
                        on_display.append((elem.string, elem.name))
                except KeyError:
                    pass

        # print on_display
        # test = map(lambda x: (x, None), [1, 2, 3, 4, 5])
        self.print_to_screen(on_display)
        # cannot use thread as Tkinter GUI can be updated from main thread only

    def print_to_canvas(self, text):
        """Print text line by line to canvas

        Text is anchored to 0.0.
        :text tuple (text, font)
        """
        # this is bad solution since canvas treats text as drawing with no
        # respect to font size
        row, col = 0, 10
        for line, font in text:
            if not font:
                font = self.font_def
            print col, row, line, font
            self.ca.create_text(col, row, text=line, anchor=NW, font=font)
            row += 20

    def print_to_screen(self, text):
        """Show text on Text widget

        Setback is no support for showing images
        """
        self.screen.config(state=NORMAL)
        self.screen.delete(0.0, END)
        tags = []
        for line, tag in text:
            # remove text identation
            #TODO - preserve last space in subs
            line = re.sub(r'\r\n[\s]*', '', line)
            self.screen.insert(CURRENT, line + '\n', tag)
            tags.append(tag)

        # turn on fonts for tagged lines
        for tag in tags:
            font = self.elem_style.get(tag, self.font_def)
            self.screen.tag_config(tag, font=font)

        self.screen.config(state=DISABLED)



win = Tk()
browser = Browser(win)

