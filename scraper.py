# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".

import scraperwiki           
import lxml.html
import lxml.etree
import pprint
html = scraperwiki.scrape("https://www.metacritic.com/music")
root = lxml.html.fromstring(html)
xp_items = lxml.etree.XPath(
    u"/".join((
        '/',
        'div[re:test(@class, "^head") and div/h2/a[re:test(text(), "Top Albums")]]',
        'following-sibling::div[@class="body"]',
        'div/ol/li[re:test(@class, "product")]'
    )),
    namespaces={"re": "http://exslt.org/regular-expressions"})
xp_item_product_title = lxml.etree.XPath('.//h3[@class="product_title"]/a')
xp_item_product_url = lxml.etree.XPath('.//h3[@class="product_title"]/a/@href')
xp_item_artist = lxml.etree.XPath('.//span[@class="product_artist"]')
xp_item_image = lxml.etree.XPath('.//img[re:test(@class, "^product_image(\s|$)")]/@src')
css_metascore = lxml.cssselect.CSSSelector("span.metascore")
#user_metascore = lxml.cssselect.CSSSelector("span.metascore_w user large album positive")
#user_basedon = lxml.etree.XPath('.//div[@class="summary"]/p/span[@class="count"]/strong')
for el in xp_items(root):
    item = {"artist": None, "title": None, "image": None, "score": None, "url": None}
    for t in xp_item_product_title (el):
        item['title'] = lxml.html.tostring(t, method="text", encoding=unicode, with_tail=False).strip(' -')
        break

    for a in xp_item_artist(el):
        item['artist'] = lxml.html.tostring(a, method="text", encoding=unicode).strip(' -')
        break

#    for i in xp_item_image (el):
#        item['image'] = i
#        break

    for s in css_metascore (el):
        item['score'] = s.text_content()
        break

    for u in xp_item_product_url(el):
        item['url'] = u
        break

    #pprint.pprint(item)
    scraperwiki.sqlite.save(unique_keys=['url'], data=item)
