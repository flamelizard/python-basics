"""Internet browser in python

Support subset of html markup nad simple rendering
- text + formatting, hyperlink, background color, image

TODO
Thread long running task to not block gui main loop

CAVEATS
- reading css often triggers some errors with charset -> commented out section
with get_external_style

Refs
http://www.thelinuxdaily.com/2011/05/python-script-to-grab-all-css-for-given-urls/
"""

from Tkinter import *
import threading
import time
import urllib2
import bs4
import re
import os
from PIL import Image, ImageTk
import urlparse
import webscrape
from collections import defaultdict


class Browser(Frame):
    def __init__(self, master, styling):
        """
        :master Tk window object
        :styling    dict for tag_name -> font style
        """
        Frame.__init__(self, master)
        self.pack(expand=YES, fill=BOTH)
        self.home_addr = 'file:///D:/git-repos/test_site/index.html'
        self.elem_style = {}
        self.elem_style.update(styling.items())
        self.style_def = ('Verdana', 10)
        self.images = []
        self.addr = self.home_addr  # current address in browser address bar
        self.url = None
        self.next_line_x = 10       # canvas position to place text/img
        self.next_line_y = 10
        self.make_widgets()
        # self.mainloop()

    def fetch_addr(self, event):
        """Fetch str from address bar"""
        # print type(event), dir(event), dir(event.widget)
        widget = event.widget
        addr = widget.get('1.0', END)
        self.addr = addr.strip()
        print 'fetch addr: ', self.addr
        self.write_addr()
        try:
            self.handle_request()
        except urllib2.URLError as e:
            self.show_line(str(e.reason))
        except Exception as e:
            self.show_line('[Error] %s, %s' % (e.message, e.args))

    def write_addr(self, addr=None):
        # reset cursor position, emulate browser behaviour
        widget = self.addr_bar
        if not addr:
            addr = self.addr

        widget.delete('1.0', END)
        widget.insert(1.0, addr)
        widget.mark_set(INSERT, '1.0')

    def make_widgets(self):
        self.addr_bar = Text(self)
        self.ca = Canvas(self)
        self.sbar = Scrollbar(self)

        self.addr_bar.config(width=70, height=1, padx=5, pady=1, bd=2)
        self.addr_bar.bind('<Return>', self.fetch_addr)
        self.addr_bar.insert('1.0', self.home_addr)
        self.ca.config(bd=2, bg='light steel blue')
        self.sbar.config(command=self.ca.yview)
        self.ca.config(yscrollcommand=self.sbar.set)
        # scroll bar does not work with unbounded canvas space - default
        self.ca.config(scrollregion=(0, 0, 1000, 5000))

        self.addr_bar.pack(fill=X)
        self.add_bookmark_bar()
        self.ca.pack(side=LEFT, expand=YES, fill=BOTH)
        self.sbar.pack(side=RIGHT, fill=Y)

    def add_bookmark_bar(self):
        home = 'www.centrum.cz'
        bar = Frame(self)
        bar.pack(fill=X)
        btn1 = Button(bar, text='Home', command=lambda: self.write_addr(home))
        btn1.pack(side=LEFT)

    def handle_request(self):
        # reset canvas to defaults
        self.ca.delete(ALL)
        self.next_line_x = 10
        self.next_line_y = 10

        scraper = webscrape.WebScrape(self.addr)
        render_tags = self.elem_style.keys()
        render_tags.sort()
        scraped = scraper.parse_tags_sequentially(render_tags)
        self.show_lines(scraped)

        # set background color from css
        # raw_css = scraper.get_external_style()
        # if raw_css:
        #     color = scraper.parse_backgr_color(raw_css)
        #     if color:
        #         _color = scraper.rgb_to_hexa(color).upper()
        #         # print '[page color] ', color, _color
        #         self.ca.config(bg=_color)

    def show_line(self, elem):
        """Print line to canvas

        :elem string or obj
        """
        img_space = 0

        if isinstance(elem, bs4.element.Tag):
            tag = elem.name
            txt = elem.string
        else:
            # arg 'elem' is pure string
            tag = None
            txt = elem
        _style = self.elem_style.get(tag, None)
        style = _style if _style else self.style_def
        pos = (self.next_line_x, self.next_line_y)

        if tag == 'img':
            img = self.try_loading_image(elem['src'])
            if img:
                self.ca.create_image(*pos, image=img, anchor=NW)
                img_space = img.height()
        elif tag == 'a':
            link = self.get_tag_attrib(elem, 'href')
            if link:
                self.ca.create_text(*pos, text=link, font=style, anchor=NW,
                                    fill='blue')
        else:
            if txt:
                txt = self.sanitize_multiline(txt)
                self.ca.create_text(*pos, text=txt, font=style, anchor=NW)

        # calc spacing between shown elements
        line_cnt = 0 if not txt else len(txt.split('\n'))
        line_height = style[1]
        text_space = (line_height+5) * line_cnt

        self.next_line_y += (text_space + img_space)

    def show_lines(self, lines):
        for line in lines:
            print line
            self.show_line(line)

    def try_loading_image(self, fpath):
        """Ad-hoc way to load images for home-grown web site

        :fpath relative file path on local filesystem
        :return tk image reference or None
        """
        root = r'd:/git-repos/test_site'
        path = os.path.join(root, fpath)
        try:
            img = Image.open(path)
            img_tk = ImageTk.PhotoImage(image=img)
            self.images.append(img_tk)
        except IOError:
            img_tk = None
        return img_tk

    def get_tag_attrib(self, tag, name):
        try:
            val = tag[name]
            # print 'tag attrib: %s, %s' % (val, type(val))
            return val
        except KeyError:
            return None

    def sanitize_multiline(self, text):
        """Remove new lines and leading/trailing space"""
        text = text.strip()
        res = [line.strip() for line in text.split('\n')]
        return '\n'.join(res)

if __name__ == '__main__':
    style = {
        'h1': ('Verdana', 20, 'bold'),
        'h2': ('Arial', 15, 'bold'),
        'p': ('Verdana', 12),
        'small': ('Verdana', 10),
        'em': ('Verdana', 10, 'italic'),
        # 'img': None,      # takes time, freezes gui
        # 'a': None,
    }
    win = Tk()
    browser = Browser(win, style)
    browser.mainloop()
