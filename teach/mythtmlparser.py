#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
#from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('handle_starttag<%s>' % tag)

    def handle_endtag(self, tag):
        print('handle_endtag</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('handle_startendtag<%s/b>' % tag)

    def handle_data(self, data):
        print('handle_data'+data)

    def handle_comment(self, data):
        print('handle_comment<!-ab-', data, '-->')

    def handle_entityref(self, name):
        print('handle_entityref&%sabc;' % name)

    def handle_charref(self, name):
        print('handle_charref&#%s;' % name)

parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
    <br/>
</body></html>''')