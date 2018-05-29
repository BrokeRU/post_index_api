import os
from dbfread import DBF
import redis
import time

redis_uri = os.environ['REDIS_URI']
redis_port = os.environ['REDIS_PORT']

r = redis.StrictRedis(host=redis_uri, port=redis_port, db=0)
table = DBF('PIndx09.dbf')

start_time = time.time()

print('Loading data...')

for record in table:
    index = record['INDEX']
    opsname = record['OPSNAME']
    opstype = record['OPSTYPE']
    opssubm = record['OPSSUBM']
    region = record['REGION']
    autonom = record['AUTONOM']
    area = record['AREA'].title()
    city = record['CITY'].title()
    city_1 = record['CITY_1'].title()
    actdate = record['ACTDATE']
    # indexold = record['INDEXOLD']

    r.hset(index, 'index', index)
    r.hset(index, 'opsname', opsname)
    r.hset(index, 'opstype', opstype)
    r.hset(index, 'opssubm', opssubm)
    r.hset(index, 'region', region)
    r.hset(index, 'autonom', autonom)
    r.hset(index, 'area', area)
    r.hset(index, 'city', city)
    r.hset(index, 'city_1', city_1)
    r.hset(index, 'actdate', actdate)
    # r.hset(index, 'indexold', indexold)

elapsed = time.time() - start_time
total = len(table)
print(f'Successfully loaded {total} rows in {elapsed} seconds.')
