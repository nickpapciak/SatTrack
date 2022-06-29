from skyfield.api import load, wgs84

from config import Config
from tles import TLE

config = Config('./config.yml')
config.populate_latlon()
tles = TLE.from_url(config.tle_url, './data/tles.txt')
now = load.timescale().now()

iss = tles[0].to_EarthSatellite()
observer = wgs84.latlon(*config.latlon)
topocentric = (iss - observer).at(now)

alt, az, distance = topocentric.altaz()

# def is_visible(sat) -> if (is nightime, alt.degrees>0, and if is_sunlit)

if alt.degrees > 0:
    print('The ISS is above the horizon')

print('Altitude:', alt)
print('Azimuth:', az)
print('Distance: {:.1f} km'.format(distance.km))







# ephemeris = load('de421.bsp')
# print(topocentric.is_sunlit(ephemeris))

# https://api.wheretheiss.at/v1/satellites/25544
# docs: https://wheretheiss.at/w/developer

# {"name":"iss","id":25544,"latitude":-1.2261282569798,"longitude":17.07716827473,"altitude":417.48282885789,"velocity":27584.215422982,"visibility":"eclipsed","footprint":4494.6349890455,"timestamp":1655946794,"daynum":2459753.5508565,"solar_lat":23.428369309737,"solar_lon":162.23298836605,"units":"kilometers"}

# API is actually about 4 seconds behind


# The maximum number of Satellite Catalog Numbers that can be encoded in a TLE is rapidly being approached with the recent commercialization of space and several key break-up events that have created a massive number of debris objects. Future adaptations of the TLE have been imagined to extend the number of encodable Satellites within the TLE.[16]


# basically, TLE is the standard to get satellite data
# NASA and NORAD provide this data based on measurements
# but it doesn't give certain types of information, as 
# result, you do some math to get, for example, satellite
# coordinates. However, this math is awful, so C algorithm 
# called SGP4 is widely used to compute these positions

# https://rhodesmill.org/skyfield/earth-satellites.html#satellite-altitude-azimuth-and-distance
# A satellite is generally only visible to a ground observer when there is still sunlight up at its altitude. The satellite will visually disappear when it enters the Earth’s shadow and reappear when it comes out of eclipse. If you are planning to observe a satellite visually, rather than with radar or radio, you will want to know which satellite passes are in sunlight. Knowing a satellite’s sunlit periods is also helpful when modeling satellite power and thermal cycles as it goes in and out of eclipse.