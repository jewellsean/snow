__author__ = 'jewellsean'

from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from db import forecast as f
from math import floor

# db connection, likely refactor out soon
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
'''
content - url2lib2 object with source of site
elevation - forecast elevation (eg. 675m)
location - forecast location (eg. whistler)

all other content is scraped from the source html code

retrive the source data
create db objects

save db to file

'''
current_datetime = datetime.now()
time_map = [datetime(current_datetime.year, current_datetime.month, current_datetime.day, 9,0,0,0),
            datetime(current_datetime.year, current_datetime.month, current_datetime.day, 15,0,0,0),
            datetime(current_datetime.year, current_datetime.month, current_datetime.day, 20,0,0,0)]

FORECAST_POINTS = 18 # 3x day for 6 days. May be 7 calendar days.


def record_snow_forecast(content, elevation, location):

    # setup in memory database
    engine = create_engine('sqlite:///foo.db', echo = False)
    Session = sessionmaker(bind = engine)
    session = Session()

    # BS4 parsing of html in
    soup = BeautifulSoup(content, "lxml")
    winds = soup.find_all('div', attrs = {'class' : 'windcell'})
    snows =  soup.find_all('td', attrs = {'class' : 'snowy'})
    rains =  soup.find_all('td', attrs = {'class' : 'rainy'})
    temperatures = parse_temperatures(soup)
    humidities = parse_humidity(soup)
    freezing_levels = parse_freezing_levels(soup)
    times = parse_times(soup)

    for forecast_interval in range(FORECAST_POINTS):
        wind_split = parse_wind(winds[forecast_interval])
        forecast = f.Forecast(collection_dateTime = current_datetime,
                              forecast_dateTime = times[forecast_interval],
                              forecast_elevation = elevation,
                              forecast_location = location,
                              wind_speed = wind_split[0],
                              wind_direction = wind_split[1],
                              snow = accumulation_str2int(snows[forecast_interval].text),
                              rain = accumulation_str2int(rains[forecast_interval].text),
                              max_temperature = temperatures[0][forecast_interval],
                              min_temperature = temperatures[1][forecast_interval],
                              chill_temperature = temperatures[2][forecast_interval],
                              humidity = humidities[forecast_interval],
                              freezing_level = freezing_levels[forecast_interval],
                              source = "snow-forecast")
        session.add(forecast)

    f.Base.metadata.create_all(engine)
    session.commit()


def accumulation_str2int(str):
    if (str == '-'):
        return 0
    else:
        return str
def parse_wind(wind):
    wind = wind.find('img')
    split = wind['alt'].split(' ')
    return split
def parse_temperatures(soup):
    temperatures = [None] * 3
    index = 0
    for temp_tags in soup.find_all('tr', attrs = {'class' : 'lar'}):
        if(temp_tags.find('span', attrs = {'class' : 'temp'}) != None):
            i = 0
            result = [None] * FORECAST_POINTS
            for parsed_temp in temp_tags.find_all('span', attrs = {'class' : 'temp'}, limit = FORECAST_POINTS):
                result[i] = parsed_temp.text
                i += 1
            temperatures[index] = result
            index += 1
    return temperatures
def parse_freezing_levels(soup):
    fl = [None] * FORECAST_POINTS
    for freeze in soup.find_all('tr', attrs = {'class' : 'lar fl'}):
        index = 0
        for freezer in freeze.find_all('span', attrs = {'class' : 'heightfl'}):
            fl[index] = freezer.text
            index += 1
    return fl
def parse_humidity(soup):
    hm = [None] * FORECAST_POINTS
    for humid in soup.find_all('tr', attrs = {'class' : 'lar rh'}):
        index = 0
        for h in humid.find_all('td'):
            hm[index] = h.text
            index += 1
    return hm
'''
1. Check to see that the first date is the correct day number as current date
2. Assemble the list of date-times for future forecasts
    - if first is morning then add +1 day on mod 3
    - if first is pm then

'''
def parse_times(soup):
    #dates = soup.find_all('td', attrs = {'class' : 'day-end'}, limit = 6)
    #if (dates[1].text.split(' ')[1] != current_datetime.day + 1):
    #    raise RuntimeError("Date error")
    times = soup.find_all('td', attrs = {'class' : 'cell'})
    start_ind = None
    if times[0].text == 'AM':
        start_ind = 0
    elif times[0].text == 'PM':
        start_ind = 1
    else:
        start_ind = 2
    times = [None] * FORECAST_POINTS
    for i in range(FORECAST_POINTS):
        index = (i + start_ind) % 3
        times[i] = time_map[index] + timedelta(hours = 24 * floor((i + start_ind)/ 3))
    return times
