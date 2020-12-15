from redis import StrictRedis
import configparser
import os

config = configparser.ConfigParser()
path = os.path.split(os.path.realpath(__file__))[0] + '/../Reptiles/db/config.conf'
print(path)
config.read(path)

drive = 'redis'


db = StrictRedis(host=config.get(drive, 'host'), port=config.get(drive, 'port'), db=config.get(drive, 'database'))
