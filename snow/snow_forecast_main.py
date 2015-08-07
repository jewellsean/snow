__author__ = 'jewellsean'

import urllib2
from scrape import snow_forecast as sf


if __name__ == "__main__":
    base_url = 'http://www.snow-forecast.com/resorts/Whistler-Blackcomb/6day/'
    #url = 'file:///Users/jewellsean/Documents/snow/bs4-practice/out.html' #debug line
    elevation_url = {'bot' : 675, 'mid' : 1480, 'top' : 2284}

    for elevation in elevation_url.keys():
        url = base_url + elevation
        content = urllib2.urlopen(url).read()
        sf.record_snow_forecast(content, elevation_url[elevation], 'whistler')
