import requests 
from requests.exceptions import ConnectionError, Timeout
import yaml

class ConfigError(Exception):
    ... 

class UnsetValue(ConfigError): 
    ...

class FileError(ConfigError): 
    ... 

def dms_to_decimal(d :int, m: int, s: int, sign: int = None) -> float: 
        '''
        Returns a dms formatted angle to decimal
        Note: all inputs should be positive
        '''
        if (d<0) or (m<0) or (s<0): 
            raise ValueError
        return (d + m/60 + s/3600)

def get_latlon_from_user() -> tuple[int]:
    '''Gets lattitude and longitude from a user input'''
    while True: 
        print('Latitude:')
        lat_dms = input('  Deg: '), input('  Min: '), input('  Sec: ')
        lat_direc = input('  N/S: ')

        print('Longitude:')
        lon_dms = input('  Deg: '), input('  Min: '), input('  Sec: ')
        lon_direc = input('  E/W: ')

        try: 
            # if they aren't all positive ints the map will fail
            lat = dms_to_decimal(*map(int, lat_dms))
            lon = dms_to_decimal(*map(int, lon_dms))
            lat_direc, lon_direc = str(lat_direc), str(lon_direc)

            # lat direction
            if lat_direc.lower() == 's': 
                lat *= -1
            elif lat_direc.lower() != 'n': 
                raise ValueError

            # lon direction
            if lon_direc.lower() == 'w': 
                lon *= -1
            elif lon_direc.lower() != 'e': 
                raise ValueError

            return lat, lon

        except ValueError: 
            print('\nInvalid input, try again...')
 
class Config: 
    def __init__(self, filepath: str): 
        self._filepath = filepath
        with open(self._filepath, 'r') as f: 
            self._config_dict = dict(yaml.safe_load(f))

    @property
    def ip_url(self): 
        return self._config_dict['ip_url']

    @property
    def tle_url(self): 
        return self._config_dict['tle_url']

    @property
    def latlon(self): 
        '''Gets the user's location in a lattitude longitude pair'''
        if self.is_set('lattitude', 'longitude'):
            return float(self._config_dict['lattitude']), float(self._config_dict['longitude'])
        raise UnsetValue('Latitude and Longitude coordinates were not set in the config.')
    
    def is_set(self, *keys: str) -> bool: 
        '''Boolean describing if all of a certain key or set of keys is set in the config'''
        for key in keys: 
            if (self._config_dict[key]) is None: 
                return False
        return True

    def write(self, key, value): 
        '''Writes the value to the key in the config'''
        if key not in self._config_dict.keys():
            raise FileError(f'Error writing to config. Key {key} is not in the config.')

        self._config_dict[key] = value
        with open(self._filepath, 'w+') as f: 
            yaml.dump(self._config_dict, f)
                
    def populate_latlon(self):
        '''Attempts to retrieve the lat/lon coords from the user and uses it to populate the config file'''
        print('Would you like to manually enter your corrdinates or retrieve your approximate ones from your ip address?')
        print('1.) Manual (default)')
        print('2.) Get from current config')
        print('3.) IP adress')
        selection = input()
        try: 
            selection = int(selection)
            if selection not in (1,2,3):
                selection = 1
        except: 
            selection = 1
    
        # manual
        if selection == 1:
            lat, lon = get_latlon_from_user()

        # config
        elif selection == 2: 
            try:
                lat, lon  = self.latlon
            except UnsetValue:
                print('Unable to read from config...')
                print('Manual input necessary.')
                lat, lon = get_latlon_from_user()

        # ip address
        else: 
            try:   
                url = self.ip_url
                response = requests.get(url, timeout=10)
                lat, lon = map(float, response.json()['loc'].split(','))
            except (ConnectionError, Timeout): 
                print('Unable to establish connection...')
                print('Manual input necessary.')
                lat, lon = get_latlon_from_user()
            
        self.write('lattitude', lat)
        self.write('longitude', lon)