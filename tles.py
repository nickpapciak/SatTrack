import requests 
from requests.exceptions import ConnectionError, Timeout
from skyfield.api import EarthSatellite, load

class TLE: 
    def __init__(self, name, l1, l2):
        self.name: str = name
        self.l1: str = l1
        self.l2: str = l2

    @classmethod
    def from_url(cls, url: str, filepath: str) -> list['TLE']: 
        '''Returns a list of TLEs from the data, attempts online retrieval but then looks for a stored backup'''
        try:
            response = requests.get(url, timeout=10)
            with open(filepath, 'w') as f:
                f.write(response.text)
            text_data = response.text.split('\r\n')

        # attempts to get tle data from stored file
        except (ConnectionError, Timeout):
            print('Error retrieving the TLE data from online, attempting to get from stored backup...')
            with open(filepath, 'r') as f: 
                text_data = f.read().split('\n\n')
        
        # sorts through recieved data and formats it according to class
        tles = []
        text_data = list(map(lambda x: x.rstrip(), text_data))
        for i in range(0, len(text_data)-3, 3): 
            name, l1, l2 = text_data[i:i+3]
            tles.append(cls(name, l1, l2))
        return tles

    def to_EarthSatellite(self): 
        '''Converts a TLE object into an EarthSatellite object'''
        return EarthSatellite(self.l1, self.l2, self.name, load.timescale())

