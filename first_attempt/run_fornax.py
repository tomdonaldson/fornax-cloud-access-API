import sys
import os

import astropy.coordinates as coord

import pyvo

sys.path.insert(0, os.getcwd())
import fornax
print(f'\nUsing fornax library in: {fornax.__file__}\n')



# do a simple sia query to chanmaster
pos = coord.SkyCoord.from_name("ngc 4151")
query_result = pyvo.dal.sia.search('https://heasarc.gsfc.nasa.gov/xamin_test/vo/sia?table=chanmaster&', pos=pos)
table_result = query_result.to_table()


# data handler
row_1 = table_result[5]
row_2 = table_result[6]

line = '+'*40
print(f'\n{line}\nData product:\n{line}')

print(row_1[['obs_id','target_name','instrument_name', 'access_format']])
print(row_2[['obs_id','target_name','instrument_name', 'access_format']])
print(f'{line}\n')


# inject a differnt region name; easier to do here than on the server
row_1['cloud_access'] = row_1['cloud_access'].replace('us-east-1', 'us-east-2')
file = fornax.AWSDataHandler(row_1).download()


# inject a differnt bucket name; easier to do here than on the server
row_2['cloud_access'] = row_2['cloud_access'].replace('heasarc', 'heasarc2')
file = fornax.AWSDataHandler(row_2).download()
