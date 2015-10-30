"""Internet browser in python

Support subset of html markup nad simple rendering
- text + formatting, hyperlink, background color, image

App Spec in progress
simple GUI
donwload web page
display text elements in GUI

TODO
clear canvas upon loading page
elements to ignore while parsing

Improvements
Thread long running task to not block gui main loop
Text screen scrollbar
Unicode support - learn basics

Branch code

Refs
http://www.thelinuxdaily.com/2011/05/python-script-to-grab-all-css-for-given-urls/
"""

"""Learnt

# BeautifulSoup

.next_elements
will walk through all elements sequencially including nested too

parsers
- html.parser is not a good one since it does not handle nicely self-closed
elements
- lxml parser is best from supported

# Tkinter

Because Tkiner is single threaded, I cannot update GUI from another than main
thread, otherwise unexpected behaviour.

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
import data_structures
import os
from PIL import Image, ImageTk
import urlparse

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class Browser(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack(expand=YES, fill=BOTH)
        self.home_addr = 'file:///D:/git-repos/test_site/index.html'
        self.elem_style = {
            'h1': ('Verdana', 20, 'bold'),
            'h2': ('Arial', 15, 'bold'),
            'p': ('Verdana', 12),
            'small': ('Verdana', 10),
            'em': ('Verdana', 10, 'italic'),
            'img': None,
            'a': None,
        }
        self.style_def = ('Verdana', 10)
        self.images = []
        self.addr = self.home_addr  # current address in browser address bar
        self.url = None
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
        self.handle_request()

    def write_addr(self, addr=None):
        # reset cursor position, emulate browser behaviour
        widget = self.addr_bar
        if not addr:
            addr = self.addr

        widget.delete('1.0', END)
        widget.insert(1.0, addr)
        widget.mark_set(INSERT, '1.0')
        # widget.mark_gravity(INSERT, LEFT)
        # print widget.index(INSERT)

    def make_widgets(self):
        self.addr_bar = Text(self)
        self.ca = Canvas(self)
        self.sbar = Scrollbar(self)
        # self.screen = Text(self)

        self.addr_bar.config(width=70, height=1, padx=5, pady=1, bd=2)
        self.addr_bar.bind('<Return>', self.fetch_addr)
        self.addr_bar.insert('1.0', self.home_addr)
        self.ca.config(bd=2, bg='light steel blue')
        self.sbar.config(command=self.ca.yview)
        self.ca.config(yscrollcommand=self.sbar.set)
        # scroll bar does not work with unbounded canvas space - default
        self.ca.config(scrollregion=(0, 0, 1000, 5000))
        # self.ca.create_text(100, 50, text='ABCEFG', font=('Arial', 20))
        # self.screen.config(height=30, bg='light steel blue')
        # self.screen.config(state=DISABLED)

        self.addr_bar.pack(fill=X)
        self.add_bookmark_bar()
        self.ca.pack(side=LEFT, expand=YES, fill=BOTH)
        self.sbar.pack(side=RIGHT, fill=Y)
        # self.screen.pack(expand=YES, fill=BOTH)

    def add_bookmark_bar(self):
        home = 'www.centrum.cz'
        bar = Frame(self)
        bar.pack(fill=X)
        btn1 = Button(bar, text='Home', command=lambda: self.write_addr(home))
        btn1.pack(side=LEFT)

    def handle_request(self):
        # worker = threading.Thread(target=lambda: self.get_page(addr))
        # # worker must put any value to self.queue to call out finish
        # worker.start()
        self.get_page()

    def get_page(self):
        # time.sleep(10)
        pref = 'file://' if self.addr.find('localhost') != -1 else 'http://'
        self.url = pref + self.addr
        reply = urllib2.urlopen(self.url)
        html = reply.read()
        reply.close()
        # print self.url, reply, dir(reply)

        on_display = []
        soup = bs4.BeautifulSoup(html, 'lxml')
        # print '[charset]', soup.original_encoding
        # soup.prettify()

        css_urls = self.parse_ext_css(soup)
        print '[css links]', css_urls

        txt = self.parse_html_soup(soup)
        # print '[parsed]', txt
        self.show_on_canvas(txt)

    def parse_ext_css(self, soup):
        """Return list of urls to external css files"""
        urls = []
        for link in soup.findAll('link', rel='stylesheet', href=True):
            url = urlparse.urljoin(self.url, link['href'])
            urls.append(url)
        return urls

    def parse_html_soup(self, soup):
        """Parse supported elements from html sequencially

        :return list of tuples (element object, text styling)
        """
        parsed = []
        for elem in soup.body.next_elements:
            if elem.name not in self.elem_style:
                continue
            # line = (elem, self.elem_style[elem.name])
            parsed.append(elem)
        return parsed

    def show_on_canvas(self, lines):
        pos_x = 10
        pos_y = 10

        for elem in lines:
            tag = elem.name
            txt = elem.string
            _style = self.elem_style[tag]
            style = _style if _style else self.style_def
            pos = (pos_x, pos_y)
            img = None

            if tag == 'img':
                img = self.try_loading_image(elem['src'])
                if img:
                    self.ca.create_image(*pos, image=img, anchor=NW)
            elif tag =='a':
                link = self.get_tag_attrib(elem, 'href')
                if link:
                    self.ca.create_text(*pos, text=link, font=style, anchor=NW,
                                        fill='blue')
            else:
                if not txt:
                    continue
                txt = self.sanitize_multiline(txt)
                self.ca.create_text(*pos, text=txt, font=style, anchor=NW)

            # calc spacing between shown elements
            line_cnt = 0 if not txt else len(txt.split('\n'))
            line_height = style[1]
            text_space = (line_height+5) * line_cnt
            img_space = img.height() if img else 0

            pos_y += (text_space + img_space)
            # print 'on canvas: %s, %s, t-%s, i-%s' % (elem, txt, text_space,
                                                     # img_space)

    # def print_to_canvas(self, text):
    #     """Print text line by line to canvas

    #     Text is anchored to 0.0.
    #     :text tuple (text, font)
    #     """
    #     # this is bad solution since canvas treats text as drawing with no
    #     # respect to font size
    #     row, col = 0, 10
    #     for line, font in text:
    #         if not font:
    #             font = self.font_def
    #         print col, row, line, font
    #         self.ca.create_text(col, row, text=line, anchor=NW, font=font)
    #         row += 20

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
browser.mainloop()

