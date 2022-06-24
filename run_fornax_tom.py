import sys
import os

import astropy.coordinates as coord

import pyvo

sys.path.insert(0, os.getcwd())
import fornax
print(f'\nUsing fornax library in: {fornax.__file__}\n')



# do a simple sia query to chanmaster
#pos = coord.SkyCoord.from_name("ngc 4151")
#query_result = pyvo.dal.sia.search('https://heasarc.gsfc.nasa.gov/xamin_test/vo/sia?table=chanmaster&', pos=pos)

pos = coord.SkyCoord.from_name("m61")
query_result = pyvo.dal.sia.search('https://mast.stsci.edu/portal_vo/Mashup/VoQuery.asmx/SiaV1?MISSION=HST&', pos=pos, size=0.0)

table_result = query_result.to_table()
access_url_column = query_result.fieldname_with_ucd('VOX:Image_AccessReference') or 'access_url'


# data handler
for data_product in table_result:
    #data_product = table_result[0]

    print(data_product[['instrument_name', 'imageFormat', 'accessURL', 'cloud_access']])

    handler = fornax.AWSDataHandler(data_product, access_url_column=access_url_column)
    handler._summary()
    #handler.download()
    handler.length_file_s3()
