'''Python for Processing Digital Elevation Models (DEMs).

Author: He Zhang @ University of Exeter
Date: 16th March 2019 (Update: 18th April 2019)
Contact: hz298@exeter.ac.uk zhangheupc@126.com

Copyright (c) 2019 He Zhang
'''

'''
DEM Data:
    EUDEMv11  -  EU-DEMv1.1
    Download Link: https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

Terms and Abbreviations:
    EPSG  -  European Petroleum Survey Group
    GCS   -  Geographic Coordinate System (Identified by an unique EPSG code)
    PCS   -  Projected Coordinate System (Identified by an unique EPSG code)
    WGS-84 [EPSG 4326]   -  1984 World Geodetic System [GCS]
    Merc [EPSG 3857]     -  Mercator -> Web Mercator -> Pseudo Mercator [PCS of WGS-84]
    OSGB-36 [EPSG 4277]  -  1936 Ordnance Survey Great Britain [GCS]
    BNG [EPSG 27700]     -  British National Grid [PCS of OSGB-36]
    ETRS-89 [EPSG 4258]  -  1989 European Terrestrial Reference System [GCS]
    LAEA [EPSG 3035]     -  Lambert Azimuthal Equal-Area [PCS of ETRS-89]
    lat  -  Latitude
    lng  -  Longitude
    Transform  -  GCS to GCS
    Project    -  GCS to PCS, PCS to PCS
    Convert    -  PCS to PCS

Functions:
    Convert DEM from LAEA PCS to ETRS-89 GCS.

    Transform DEM from ETRS-89 GCS to WGS-84 GCS.
    Transform DEM from ETRS-89 GCS to OSGB-36 GCS.

    Get the elevation from DEM in WGS-84 GCS.
    Get the elevation from DEM in OSGB-36 GCS.
    Get the elevation from DEM in ETRS-89 GCS.

******************** Important Information of Code Usage ********************
- Use 'GDAL.GetProjection()' to check the GCS/PCS information of DEM (in TIF format).
- Use 'GDAL.GetGeoTransform()' to check the resolution of DEMs.
- Use 'GDAL.GetGeoTransform()' to check (lat, lng) of top-left corner of DEM (in GCS).
- The (lat, lng) of other locations in DEM can therefore be calculated.
- Each GCS has one related PCS (GCS/PCS is identified by an unique EPSG code).
- You can transform DEM between different GCSs (e.g., WGS-84 <-> OSGB-36 <-> ETRS-89).
- You can project DEM in GCS to the related PCS and then display its 2D image.
- You can not display DEM in GCS as 2D image (e.g., WGS-84 -> 2D image is wrong).
- You can not project DEM in GCS to the unrelated PCS (e.g., WGS-84 -> BNG is wrong).
- You can not project DEM between different PCSs (e.g., Pseudo Mercator <-> BNG is wrong).
* Use 'gdalwarp' command to transform/project DEM to different GCSs/PCSs might be correct.
'''

# Python 3.7

# import os
# import re
# import shutil
# import subprocess

# import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
from pandas import read_csv

from pyDEM_function import get_dem_info
from pyDEM_function import get_elevation
# from pyDEM_function import get_file_names
# from pyDEM_function import show_2d_dem
from pyDEM_function import transprojcnvt_dem
# from pyDEM_function import write_dem


# Specify user settings.

# Set the EPSG code.
EPSG_WGS84 = 4326
EPSG_OSGB36 = 4277
EPSG_ETRS89 = 4258
EPSG_LAEA = 3035

# Set the format of DEMs.
DEM_FORMAT = '.tif'

# Set the path of DEMs.
PATH_EUDEM = 'DATA/DATA_EUDEMv11/'
# PATH_EUDEM_SOURCE = 'DATA/DATA_EUDEMv11/EPSG3035_s/'  # The folder of source DEMs must exist.

# Set the name of DEMs in GCSs.
EUDEM_GCS_WD = 'EUDEMv11_EPSG4326.tif'
EUDEM_GCS_UK = 'EUDEMv11_EPSG4277.tif'
EUDEM_GCS_EU = 'EUDEMv11_EPSG4258.tif'

# Set the name of DEMs in PCSs.
EUDEM_PCS_WD = 'EUDEMv11_EPSG3857.tif'
EUDEM_PCS_UK = 'EUDEMv11_EPSG27700.tif'
EUDEM_PCS_EU = 'EUDEMv11_EPSG3035.tif'

# Set the path of location data file.
PATH_LD_STATION_DATA = 'DATA/DATA_LD_AirQuality/London_AirQuality_Stations.csv'


# <EUDEMv11> Convert DEM from LAEA PCS to ETRS-89 GCS.

print('\n>>> <EUDEMv11> Convert DEM from LAEA PCS to ETRS-89 GCS.')

path = PATH_EUDEM
dem_in = path + EUDEM_PCS_EU
dem_out = path + EUDEM_GCS_EU

epsg_in = EPSG_LAEA
epsg_out = EPSG_ETRS89

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# <EUDEMv11> Transform DEM from ETRS-89 GCS to WGS-84 GCS.

print('\n>>> <EUDEMv11> Transform DEM from ETRS-89 GCS to WGS-84 GCS.')

path = PATH_EUDEM
dem_in = path + EUDEM_GCS_EU
dem_out = path + EUDEM_GCS_WD

epsg_in = EPSG_ETRS89
epsg_out = EPSG_WGS84

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# <EUDEMv11> Transform DEM from ETRS-89 GCS to OSGB-36 GCS.

print('\n>>> <EUDEMv11> Transform DEM from ETRS-89 GCS to OSGB-36 GCS.')

path = PATH_EUDEM
dem_in = path + EUDEM_GCS_EU
dem_out = path + EUDEM_GCS_UK

epsg_in = EPSG_ETRS89
epsg_out = EPSG_OSGB36

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# Read London air quality monitoring station data file.

print('\n>>> Read London air quality monitoring station data file.')

site_data = read_csv(PATH_LD_STATION_DATA)
print(site_data.head(3))

site_num = site_data['SiteName'].count()
print('\n*==> The number of stations is: %d' % site_num)

# Get the latitude and longitude of stations.
site_latlng = np.zeros((site_num, 2))
site_latlng[:, 0] = site_data['Latitude']  # The 0-th column - Latitude.
site_latlng[:, 1] = site_data['Longitude']  # The 1-th column - Longitude.

np.set_printoptions(suppress=True)  # Print numbers without scientific notation.
print('\n*==> The location (lat, lng) of stations are:\n', site_latlng)

print('\n>>> Complete!\n')


# <EUDEMv11> Get the elevation from DEM in WGS-84 GCS.

print('\n>>> <EUDEMv11> Get the elevation from DEM in WGS-84 GCS.')

dem_gcs = gdal.Open(PATH_EUDEM + EUDEM_GCS_WD)
get_dem_info(dem_gcs, 1)

site_ele_eudem_wgs = get_elevation(dem_gcs, site_latlng)
np.set_printoptions(suppress=True)

print('\n*==> The elevation information of stations is:\n', site_ele_eudem_wgs)
print('\n*==> The elevation value of stations is:\n', site_ele_eudem_wgs[:, 5].astype(int))

print('\n>>> Complete!\n')


# <EUDEMv11> Get the elevation from DEM in OSGB-36 GCS.

print('\n>>> <EUDEMv11> Get the elevation from DEM in OSGB-36 GCS.')

dem_gcs = gdal.Open(PATH_EUDEM + EUDEM_GCS_UK)
get_dem_info(dem_gcs, 1)

site_ele_eudem_osgb = get_elevation(dem_gcs, site_latlng)
np.set_printoptions(suppress=True)

print('\n*==> The elevation information of stations is:\n', site_ele_eudem_osgb)
print('\n*==> The elevation value of stations is:\n', site_ele_eudem_osgb[:, 5].astype(int))

print('\n>>> Complete!\n')


# <EUDEMv11> Get the elevation from DEM in ETRS-89 GCS.

print('\n>>> <EUDEMv11> Get the elevation from DEM in ETRS-89 GCS.')

dem_gcs = gdal.Open(PATH_EUDEM + EUDEM_GCS_EU)
get_dem_info(dem_gcs, 1)

site_ele_eudem_etrs = get_elevation(dem_gcs, site_latlng)
np.set_printoptions(suppress=True)

print('\n*==> The elevation information of stations is:\n', site_ele_eudem_etrs)
print('\n*==> The elevation value of stations is:\n', site_ele_eudem_etrs[:, 5].astype(int))

print('\n>>> Complete!\n')


# Compare the elevation obtained from different DEMs.

print('\n>>> Compare the elevation obtained from different DEMs.')

print('\nEUDEMv11_WD', site_ele_eudem_wgs[:, 5].astype(int))
print('\nEUDEMv11_UK', site_ele_eudem_osgb[:, 5].astype(int))
print('\nEUDEMv11_EU', site_ele_eudem_etrs[:, 5].astype(int))

print('\n>>> Complete!\n')
