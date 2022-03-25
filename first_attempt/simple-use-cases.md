## Introduction
This notebook contains the basic use case of querying and downloading data from the three archives: HEASARC, MAST and IRSA using either `astroquery` or `pyvo`.

In each case, a simple search for some source (`NGC 4151`) is done, and an attempt at downloading the data is made.


```python
import os
import sys

import astroquery
import pyvo
import astropy.coordinates as coord
from astropy import units
from astropy.utils.data import download_file
```

## Astroquery

### Heasarc


```python
from astroquery import heasarc

#tables = heasarc.Heasarc.query_mission_list()
res_heasarc = heasarc.Heasarc.query_object('NGC 4151', mission='chanmaster', fields='All')
print(res_heasarc.colnames)
```

    ['OBSID', 'STATUS', 'NAME', 'RA', 'DEC', 'TIME', 'DETECTOR', 'GRATING', 'EXPOSURE', 'TYPE', 'PI', 'PUBLIC_DATE', 'BII', 'CATEGORY', 'CLASS', 'CYCLE', 'DATA_MODE', 'LII', 'PROPOSAL', 'SEQUENCE_NUMBER', 'SEARCH_OFFSET_']


<p style="background:#fdd;border-color:#faa;border-style: solid;padding:10px">
<b>There is NO link to the data.</b>
</p>

### Mast


```python
from astroquery import mast

res_mast = mast.Observations.query_object('NGC 4151')
print(res_mast.colnames)
```

    ['intentType', 'obs_collection', 'provenance_name', 'instrument_name', 'project', 'filters', 'wavelength_region', 'target_name', 'target_classification', 'obs_id', 's_ra', 's_dec', 'dataproduct_type', 'proposal_pi', 'calib_level', 't_min', 't_max', 't_exptime', 'em_min', 'em_max', 'obs_title', 't_obs_release', 'proposal_id', 'proposal_type', 'sequence_number', 's_region', 'jpegURL', 'dataURL', 'dataRights', 'mtFlag', 'srcDen', 'obsid', 'distance']



```python
# we have `dataURL` and `jpegURL`, so we can download the data.
# download_file(res_mast[0]['dataURL'])
```

<br/>
To get more products, we can call `mast.Observations.get_product_list`, which queries the mast API for a list of products given the `obs_id` extracted from the table returned by `mast.Observations.query_*`. Doing that, we obtain a list of all related data products, each having a `dataURI` field that starts with: `mast:...`


```python
prod = mast.Observations.get_product_list(res_mast[0])
print(prod.colnames)
print(prod['dataURI'][:3])
```

    ['obsID', 'obs_collection', 'dataproduct_type', 'obs_id', 'description', 'type', 'dataURI', 'productType', 'productGroupDescription', 'productSubGroupDescription', 'productDocumentationURL', 'project', 'prvversion', 'proposal_id', 'productFilename', 'size', 'parent_obsid', 'dataRights', 'calib_level']
                                        dataURI                                    
    -------------------------------------------------------------------------------
    mast:WUPPE/url/pub/astro/wuppe/data/ngc4151_811611_2/ngc4151_811611_2_hw.txt.gz
        mast:WUPPE/url/pub/browse/previews/astro/wuppe/gif/ngc4151_811611_2_hwa.gif
        mast:WUPPE/url/pub/browse/previews/astro/wuppe/gif/ngc4151_811611_2_hwe.gif


<br/>
To convert the `dataURI` to an address, the `mast` module in `astroquery` prepends the address: `https://mast.stsci.edu/api/v0.1/Download/file?uri=` to download the data.

<p style="background:#dfd;border-color:#afa;border-style: solid;padding:10px">
The same dataURI is used in `astroquey.mast` to obtain the cloud address by again calling an API at https://mast.stsci.edu/api/v0.1/path_lookup/ to convert the URI to a path. Given this path, and a hard-coded backet name, the full path to the file in the cloud is obtained.
</p>

### IRSA


```python
from astroquery.ipac import irsa, ned

pos = coord.SkyCoord.from_name("ngc 4151")
#irsa.Irsa.print_catalogs()
res_irsa = irsa.Irsa.query_region(pos, radius=coord.Angle(1*units.arcmin), catalog='allwise_p3as_psd')
print(res_irsa.colnames)
```

    ['designation', 'ra', 'dec', 'clon', 'clat', 'sigra', 'sigdec', 'sigradec', 'w1mpro', 'w1sigmpro', 'w1snr', 'w1rchi2', 'w2mpro', 'w2sigmpro', 'w2snr', 'w2rchi2', 'w3mpro', 'w3sigmpro', 'w3snr', 'w3rchi2', 'w4mpro', 'w4sigmpro', 'w4snr', 'w4rchi2', 'nb', 'na', 'w1sat', 'w2sat', 'w3sat', 'w4sat', 'pmra', 'sigpmra', 'pmdec', 'sigpmdec', 'cc_flags', 'ext_flg', 'var_flg', 'ph_qual', 'moon_lev', 'w1nm', 'w1m', 'w2nm', 'w2m', 'w3nm', 'w3m', 'w4nm', 'w4m', 'dist', 'angle']


<p style="background:#fdd;border-color:#faa;border-style: solid;padding:10px">
It looks like only catalogs are available through astroquery. <b>There is NO link to the data.</b>
</p>

---
## PyVO
We use the SIA protocol to find images


```python
# these will be used by all archive queries below
services = pyvo.regsearch(servicetype='image')
pos = coord.SkyCoord.from_name("ngc 4151")
```

### Heasarc


```python
# we use chanmaster data
svc_heasarc = [s for s in services if 'heasarc' in s.ivoid][2]
print(svc_heasarc.access_url)
```

    https://heasarc.gsfc.nasa.gov/xamin/vo/sia?table=chanmaster&



```python
# search for the source
vo_res_heasarc = svc_heasarc.search(pos=pos)
```


```python
print(vo_res_heasarc.fieldnames)
```

    ('obsid', 'status', 'name', 'ra', 'dec', 'time', 'detector', 'grating', 'exposure', 'type', 'pi', 'public_date', 'datalink', 't_min', 't_resolution', 't_max', 't_exptime', 'em_res_power', 's_ra', 's_dec', 's_resolution', 'access_estsize', 's_fov', 's_region', 'o_ucd', 'access_url', 'obs_publisher_did', 'dataproduct_type', 'obs_id', 'obs_collection', 'target_name', 'instrument_name', 'facility_name', 'pol_states', 'calib_level', 'access_format', 'em_min', 'em_max', 'SIA_title', 'SIA_scale', 'SIA_naxis', 'SIA_naxes', 'SIA_format', 'SIA_reference', 'SIA_ra', 'SIA_dec', 'SIA_instrument')


<br/>
These tables have a `access_url` field that can used to download the data



```python
print(vo_res_heasarc['access_url'][:3])
```

    ['https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/8/15158/primary/acisf15158N003_cntr_img2.fits.gz'
     'https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/8/15158/primary/acisf15158N003_cntr_img2.jpg'
     'https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/0/3480/primary/acisf03480N004_cntr_img2.jpg']



```python
#download_file(vo_res_heasarc[0]['access_url'])
```

<br/>
In this case, the service also provides a datalinks for each row, which provide many data products that are related to the selected row.



```python
# and we can get the datalinks
dl_heasarc = vo_res_heasarc[0].getdatalink()
print(dl_heasarc['access_url'])
```

    ['https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/8//15158/primary/acisf15158N003_cntr_img2.fits.gz'
     'https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/8//15158/primary/acisf15158N003_full_img2.fits.gz'
     'https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/8//15158/primary/acisf15158N003_cntr_img2.jpg'
     'https://heasarc.gsfc.nasa.gov/FTP/chandra/data/byobsid/8//15158/primary/acisf15158N003_full_img2.jpg']


<br/>

<p style="background:#dfd;border-color:#afa;border-style: solid;padding:10px">
This means that the archive can serve the cloud link, when available, as another datalink for each search row. There is a lot of flexibility here, as one can add as many datalinks as needed.
</p>

### Mast


```python
#[s.ivoid for s in services if 'stsci' in s.ivoid]
# galex
svc_mast = [s for s in services if 'stsci' in s.ivoid][2]
print(svc_mast.access_url)
```

    https://mast.stsci.edu/portal/Mashup/VoQuery.asmx/SiaV1?MISSION=GALEX&



```python
vo_res_mast = svc_mast.search(pos=pos)
print(vo_res_mast.fieldnames)
```

    ('collection', 'insname', 'name', 'trgPosRA', 'trgPosDec', 'contentlength', 'midpoint', 'naxes', 'naxis', 'scale', 'contenttype', 'coordFrame', 'projection', 'crpix', 'crval', 'cdmatrix', 'enremband', 'enrUnits', 'enrValue', 'enrMax', 'enrMin', 'accessURL')


<br/>

These tables have a `accessURL` field that can used to download the data



```python
print(vo_res_mast['accessURL'][:3])
```

    ['http://galex.stsci.edu/data/GR6/pipe/02-vsn/50107-AIS_107/d/00-visits/0001-img/07-try/qa/AIS_107_0001_sg66-xd-int_2color.jpg'
     'http://galex.stsci.edu/data/GR6/pipe/02-vsn/50107-AIS_107/d/00-visits/0001-img/07-try/qa/AIS_107_0001_sg66-xd-int_2color_large.jpg'
     'http://galex.stsci.edu/data/GR6/pipe/02-vsn/50107-AIS_107/d/00-visits/0001-img/07-try/qa/AIS_107_0001_sg55-xd-int_2color.jpg']



```python
# download_file(vo_res_mast[0]['accessURL'])
```

<br/>

<p style="background:#dfd;border-color:#afa;border-style: solid;padding:10px">
These don't provide any datalinks. Cloud links may need datalinks to be implemented, or some API that translates the http link to a cloud access, somewhat similar to the one currently implimented by astroquery.mast
</p>

### Irsa


```python
#[s.ivoid for s in services if 'irsa' in s.ivoid and 'wise/images/allwise/l3a' in s.ivoid]
# wise
svc_irsa = [s for s in services if 'irsa' in s.ivoid and 'wise/images/allwise/l3a' in s.ivoid][0]
print(svc_irsa.access_url)
```

    https://irsa.ipac.caltech.edu/ibe/sia/wise/allwise/p3am_cdd?



```python
vo_res_irsa = svc_irsa.search(pos=pos)
print(vo_res_irsa.fieldnames)
```

    ('sia_title', 'sia_url', 'sia_naxes', 'sia_fmt', 'sia_ra', 'sia_dec', 'sia_naxis', 'sia_crpix', 'sia_crval', 'sia_proj', 'sia_scale', 'sia_cd', 'sia_bp_id', 'sia_bp_ref', 'sia_bp_hi', 'sia_bp_lo', 'magzp', 'magzpunc', 'unc_url', 'cov_url', 'coadd_id')


<br/>

These tables have a `sia_url` field that can used to download the data



```python
print(vo_res_irsa['sia_url'][:3])
```

    ['https://irsa.ipac.caltech.edu/ibe/data/wise/allwise/p3am_cdd/18/1838/1838p393_ac51/1838p393_ac51-w1-int-3.fits'
     'https://irsa.ipac.caltech.edu/ibe/data/wise/allwise/p3am_cdd/18/1838/1838p393_ac51/1838p393_ac51-w3-int-3.fits'
     'https://irsa.ipac.caltech.edu/ibe/data/wise/allwise/p3am_cdd/18/1838/1838p393_ac51/1838p393_ac51-w2-int-3.fits']



```python
# download_file(vo_res_irsa[0]['sia_url'])
```

<br/>

<p style="background:#dfd;border-color:#afa;border-style: solid;padding:10px">
Similar to MAST, there are no datalinks. Cloud links may need datalinks to be implemented, or some API that translates the http link to a cloud link, somewhat similar to the one currently implimented by astroquery.mast.
</p>
