import unittest
import webscrape
import urllib2
import bs4


class WebscrapeTester(unittest.TestCase):
    def setUp(self):
        self.scrape = webscrape.WebScrape('test_address', get_now=False)
        self.scrape.test_load_raw_html(test_html)

    # Pass to assertRaises ref to function !
    def test_no_address_exception(self):
        self.assertRaises(urllib2.URLError, webscrape.WebScrape,
                          'sillyaddress.aa', get_now=True)

    def test_simple_parsing(self):
        all_tags = ['html', 'head', 'title', 'body', 'h1', 'h2', 'p', 'ul', 'li']

        self.assertEqual(0, len(self.scrape.parse_tags(['img', 'h3'])))
        self.assertEqual(3, len(self.scrape.parse_tags(['h1', 'p', 'style'])))

        self.assertIsNone(self.scrape.get_external_style())

        tags = self.scrape.parse_tags_sequentially(['h1', 'h2', 'ul'])
        self.assertListEqual(['h1', 'h2', 'ul'], [tag.name for tag in tags])

        tags = self.scrape.parse_tags(all_tags)
        self.assertIsInstance(tags['li'][0], bs4.element.Tag)
        self.assertEqual(3, len(tags['li']))

test_html = """
<html>
<head>
<title>Test HTML code</title>
<style>
    html {
        background-color: rgb(255, 0, 0);
    }
</style>
</head>
<body>
<h1>Factory</h1>
<p class="main">We build hammers</p>
<h2>About us</h2>
<strong>Long history of making hammers with your own branding</strong>
<ul>
<li>golden hammer</li>
<li>stainless steel hammer</li>
<li>rubber hammer for highest safety</li>
</ul>
</body>
</html>
"""

if __name__ == '__main__':
    unittest.main()
