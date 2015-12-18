import logging, sys, os, codecs

import requests, cache, csv
from bs4 import BeautifulSoup

BASE_URL = "http://www.nuforc.org/webreports/"  # needed to reconstruct relative URLs
START_PAGE = "ndxshape.html" # uses shape page because least # requests to get all the data
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Where the resulting csv file will be created

# set up CSV file
UFO_DATA_CSV = open(BASE_DIR + 'ufodata.csv','wb')
fieldnames = ["date_time", "city", "state", "shape", "duration", "summary", "date_posted"]
csvwriter = csv.DictWriter(UFO_DATA_CSV, delimiter=',', fieldnames=fieldnames)
csvwriter.writeheader()

class DictUnicodeProxy(object):
    def __init__(self, d):
        self.d = d
    def __iter__(self):
        return self.d.__iter__()
    def get(self, item, default=None):
        i = self.d.get(item, default)
        if isinstance(i, unicode):
            return i.encode('utf-8')
        return i

def getColFromIndex(x):
    return {
        0 : 'date_time',
        1: 'city',
        2: 'state',
        3: 'shape',
        4: 'duration',
        5: 'summary',
        6:'date_posted'
    }.get(x, 0) 

# set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# let's scrape
url = BASE_URL + START_PAGE
logger.info("Scraping UFO reports from %s" % url)

# first grab the index page
if not cache.contains(url):
    index_page = requests.get(url)
    logger.debug("\tadded to cache from %s" % url)
    cache.put(url, index_page.text)
content = cache.get(url)

# now pull out all the links to songs
dom = BeautifulSoup(content)

#/html/body/p/table/tbody/tr[1]/td[1]/font/a

link_tags = dom.select("td a")
logger.debug("\tfound %d link tags" % len(link_tags))
links = set([ tag['href'] for tag in link_tags ])   # get all the unique urls
logger.info("\tfound %d links to UFO shapes" % len(links))

# now scrape ufo data from each page that lists reports
tr_count = 0
for ufo_shape_link in links:
    shape_url = BASE_URL + ufo_shape_link
    if not cache.contains(shape_url):
        shape_page = requests.get(shape_url)
        logger.debug("\tadded to cache from %s" % shape_url)
        cache.put(shape_url,shape_page.text)
    content = cache.get(shape_url)
    dom = BeautifulSoup(content)
   
    table_rows = dom.select("tr")
    tr_count += len(table_rows)
    for row in table_rows:
        new_row = {}
        cols = row.select("td")
        i = 0;
        for col in cols:
            col_name = getColFromIndex(i)
            new_row[col_name] = col.getText()
            i+=1
        csvwriter.writerow(DictUnicodeProxy(new_row))

logger.info("Done (scraped %d rows)!",tr_count)


'''if dom.select("#b p:nth-of-type(2)") is not None and len(dom.select("#b p:nth-of-type(2)")) > 0:
        lyrics_tags = dom.select("#b p:nth-of-type(2)")[0].children
        lyrics = [child for child in lyrics_tags if child.name!="br"]
        for line in lyrics:
            lyrics_file.write(line+os.linesep)
            line_count = line_count + 1'''
'''

lyrics_file = codecs.open("lyrics-"+artist+".txt", 'w', 'utf-8')
for relative_song_url in links:
    song_url = BASE_URL + relative_song_url
    if not cache.contains(song_url):
        song_page = requests.get(song_url)
        logger.debug("\tadded to cache from %s" % song_url)
        cache.put(song_url,song_page.text)
    content = cache.get(song_url)
    dom = BeautifulSoup(content)
    if dom.select("#b p:nth-of-type(2)") is not None and len(dom.select("#b p:nth-of-type(2)")) > 0:
        lyrics_tags = dom.select("#b p:nth-of-type(2)")[0].children
        lyrics = [child for child in lyrics_tags if child.name!="br"]
        for line in lyrics:
            lyrics_file.write(line+os.linesep)
            line_count = line_count + 1

logger.info("Done (scraped %d lines)!",line_count)
'''