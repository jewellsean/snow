__author__ = 'jewellsean'

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()

''''
Assumes data is collected on standard PST time (could change to UTC)

Assumes metric with the following base units

temperatures (degree C)
elevation (m)
wind speed (km/h)

snow (cm)
rain (mm)


time conversions

am -- 09h00
pm -- 15h00
night -- 20h00

'''
class Forecast(Base):
    __tablename__ = 'forecast'
    id = Column(Integer, primary_key= True)
    collection_dateTime = Column(DateTime)
    forecast_dateTime = Column(DateTime)
    forecast_elevation = Column(Integer)
    forecast_location = Column(String)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    snow = Column(Float)
    rain = Column(Float)
    max_temperature = Column(Float)
    min_temperature = Column(Float)
    chill_temperature = Column(Float)
    humidity = Column(Float)
    freezing_level = Column(Integer)
    source = Column(String)

    # if (snow < 0):
    #     raise ValueError("Amount of snow (cm) must be positive", snow)
    # if (rain < 0):
    #     raise ValueError("Amounnt of rain (mm) must be positive", rain)
    # if (wind_speed < 0):
    #     raise ValueError("Wind speed must be positive", wind_speed)
    # if (forecast_elevation < 0):
    #     raise ValueError("Please predict above sea-level. Forecast elevation must be positve", forecast_elevation)
    # if (max_temperature < min_temperature):
    #     raise ValueError("Max temperature must be greater than min temperature", max_temperature, min_temperature)
    # if (humidity < 0):
    #     raise ValueError("Humidity must be >= than 0")
    # if (freezing_level < 0):
    #     raise ValueError("Freezing level must be >= 0")



