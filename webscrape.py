"""
download web page
donwload css files
parse elements in list

urlopen
error 'no host given'
    urlunparse returned scheme with '///' instead of '//'

TODO
way to search through python standard lib to find quickly reaal world usage of
some pattern like @property, print first 10 or random lines
"""
import urlparse
import urllib2
import bs4
from collections import defaultdict

def print_attrib(o):
    lst = []
    for attr in dir(o):
        try:
            val = str(getattr(o, attr))
            lst.append((attr, val))
        except AttributeError:
            pass
    for attr, val in lst:
        print '%s -> %s' % (attr, val)

class WebScrape(object):
    def __init__(self, addr):
        self._url = self.normalize_url(addr)
        self.soup = None
        self.parser = 'lxml'
        # print '[attrib]', self.url
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

    def scrape_page(self):
        """Download and slurp markup to var soup"""
        html = self.download_page()
        if html:
            self.soup = self.parse_html(html)
        # print self.soup.prettify()
        # print self.get_external_style()
        # print self.get_inline_style()
        # print self.parse_tags(['p', 'a'])

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
        try:
            reply = urllib2.urlopen(url=url)
        except urllib2.URLError as e:
            print 'Error: %s' % e.reason
            return None
        # assert isinstance(reply, urllib2.addinfourl)
        html = reply.read()
        reply.close()
        return html

    def parse_html(self, html):
        return bs4.BeautifulSoup(html, self.parser)
        # print '[charset]', soup.original_encoding
        # soup.prettify()

    def get_external_style(self):
        """
        :return stylesheet as string
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
            raw_css += self.download_page(ref)
        return raw_css

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
    # scraper = WebScrape('file:///D:/git-repos/test_site/css_robot.html')
    elems = scraper.parse_tags_sequentially(['h1', 'h2', 'p'])
    for elem in elems:
        print elem

    scraper.url = 'bob'
    print scraper.soup
