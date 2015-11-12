"""
webscrape.py

Class WebScrape to scrape off HTML/CSS content on a single page
- donwload content
- parse content for custom tags

Errors
urllib2, error 'no host given'
    urlunparse returned scheme with '///' instead of '//'

Raises
    urllib2.URLError
"""

import urlparse
import urllib2
import bs4
from collections import defaultdict
import tinycss
import tinycss.color3

class WebScrape(object):
    def __init__(self, addr, get_now=None):
        self._url = self.normalize_url(addr)
        self.soup = None
        self.parser = 'lxml'
        if get_now:
            self.scrape_page()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, addr):
        if hasattr(self, 'soup'):
            self.soup = None
        self._url = self.normalize_url(addr)
        self.scrape_page()

    def test(self):
        pass

    def test_load_raw_html(self, html):
        """Use raw html instead of downloading a page

        Supposed for unittest only
        """
        if html:
            self.soup = self.parse_html(html)

    def _parse_css(self, raw_css):
        """Simply example on using tinycss

        Print properties for selector 'body'
        Refer to link below for exact CSS terminology, important to use module
        effectively.
        http://www.w3.org/TR/CSS21/syndata.html#tokenization

        :raw_css
            css stylesheet as unicode string
        """
        # parser defaults to CSS2.1
        parser = tinycss.make_parser()
        # parser can accept data through multiple ways
        stylesheet = parser.parse_stylesheet(raw_css)
        # rule set (or rule) is a selector and declarations block
        # e.g 'html' { font-size: 1px; font-color: 'green'}
        for rule in stylesheet.rules:
            # data units are often in form of class Token
            #.as_css() returns string repr
            if rule.selector.as_css() == 'body':
                for declar in rule.declarations:
                    # assert isinstance(declar.value, tinycss.token_data.TokenList)
                    print '%s -> %s' % (declar.name, declar.value.as_css())

    def parse_backgr_color(self, raw_css):
        """
        :return tuple rgb() for 'html' or 'body', None for no color
        """
        parser = tinycss.make_parser()
        stylesheet = parser.parse_stylesheet(raw_css)
        for rule in stylesheet.rules:
            if rule.selector.as_css() in ['html', 'body']:
                for declar in rule.declarations:
                    # assert isinstance(declar.value, tinycss.token_data.TokenList)
                    if declar.name == 'background-color':
                        # parse color value to single format as tuple rgb()
                        return tinycss.color3.parse_color(declar.value[0])
                        # return declar.value.as_css()
        return None

    def rgb_to_hexa(self, color):
        """Convert color from rgb() to hexadecimal

        :color tuple rgb(), each value in range 0-1
        """
        hexa = ''
        for col in color[:3]:
            hexa += '{:02x}'.format(int(col * 255))
        return '#{}'.format(hexa)

    def scrape_page(self, raw_html=None):
        """Download and slurp markup to var soup"""
        html = self.download_page()
        if html:
            self.soup = self.parse_html(html)
        # print self.soup.prettify()

    def normalize_url(self, url):
        """
        :return url string

        Important - valid address must begin with '//'.
        Oterwise, URL is considered path instead of netloc (e.g www.google.com).
        This will cause URL to start with '///' upon urlunparse or urlunsplit.
        """
        o = urlparse.urlparse(url)
        if not o.scheme:
            url = 'http://' + url
        return url

    def download_page(self, url=None):
        """
        :return html markup or None
        """
        if not url:
            url = self.url
        reply = urllib2.urlopen(url=url)
        # assert isinstance(reply, urllib2.addinfourl)
        html = reply.read()
        reply.close()
        return html

    def parse_html(self, html):
        return bs4.BeautifulSoup(html, self.parser)
        # print '[charset]', soup.original_encoding

    def get_external_style(self):
        """
        :return stylesheet as string or None
        """
        refs = []
        for link in self.soup.find_all('link', rel='stylesheet', href=True):
            o = urlparse.urlparse(link['href'])
            # is relative link?
            if not o.scheme and not o.netloc:
                refs.append(urlparse.urljoin(self.url, o.path))
            else:
                refs.append(o.geturl())
        raw_css = ''
        for ref in refs:
            # print '[ref]', ref
            _css = self.download_page(ref)
            if _css:
                raw_css += _css
        return raw_css if raw_css else None

    def get_inline_style(self):
        """
        :return stylesheet as string
        """
        raw_css = ''
        for style in self.soup.find_all('style'):
            raw_css += style.string
        return raw_css

    def parse_tags(self, tags):
        """
        :return dict of tag name <-> tag objects found
        """
        found = defaultdict(list)
        for name in tags:
            for tag in self.soup.find_all(name=name):
                found[name].append(tag)
                # assert isinstance(tag, bs4.element.Tag)
                # print 'parsed tags', tag.__class__
        return found

    def parse_tags_sequentially(self, tags):
        """Parse tags in list tags from html as they occur

        :return list of parsed tag objects
        """
        parsed = []
        for tag in self.soup.body.next_elements:
            if tag.name in tags:
                parsed.append(tag)
        return parsed


if __name__ == '__main__':
    scraper = WebScrape('file:///D:/git-repos/test_site/index.html')
    elems = scraper.parse_tags_sequentially(['h1', 'h2', 'p'])
    for elem in elems:
        print elem
    # test
    scraper.test()
