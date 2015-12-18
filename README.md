UFO Data Scraper
=====================

This is a very simple web scraper based on @rahulbot's [lyrics-123 scraper](https://github.com/rahulbot/lyrics123-scraper) that pulls down UFO sightings and puts them into a CSV file for students to analyze in the classroom (data is fun!).  Content is pulled from the [National UFO Reporting Center's index of UFO reports by shape](http://www.nuforc.org/webreports/ndxshape.html).

Installation
------------

```
pip install -r requirements.pip
```

Using
-----

Just run scrape.py and make sure you have an internet connection.  This script will create an output `.csv` file with all the combined UFO reports.

For example:
```
python scrape.py 
```
