#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''Process Digital Elevation Models (DEMs) with Python.

Author: He Zhang @ University of Exeter
Date: Mar 16th 2019
Contact: hz298@exeter.ac.uk

DEM Data:
    ASTGDEMv20  -  ASTER-GDEMv2.0
    Download Link: https://earthexplorer.usgs.gov/

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
    Remove the overlapped elements of DEMs in WGS-84 GCS.
    Merge the reformed DEMs in WGS-84 GCS.

    Transform the merged DEM from WGS-84 GCS to OSGB-36 GCS.
    Transform the merged DEM from WGS-84 GCS to ETRS-89 GCS.

    Project DEM from WGS-84 GCS to Pseudo Mercator PCS.
    Project DEM from OSGB-36 GCS to BNG PCS.
    Project DEM from ETRS-89 GCS to LAEA PCS.

    Display 2D DEM image in Pseudo Mercator PCS.
    Display 2D DEM image in BNG PCS.
    Display 2D DEM image in LAEA PCS.

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

import os
import re
import shutil
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
from pandas import read_csv

from pyDEM_function import get_dem_info
from pyDEM_function import get_elevation
from pyDEM_function import get_file_names
from pyDEM_function import show_2d_dem
from pyDEM_function import transprojcnvt_dem
from pyDEM_function import write_dem


# In[2]:


# Specify user settings.

# Set the format of DEMs.
DEM_FORMAT = '.tif'

# Set the path of DEMs.
PATH_ASTGDEM = "DATA/DATA_ASTGDEMv20/"
PATH_ASTGDEM_SOURCE = "DATA/DATA_ASTGDEMv20/EPSG4326_s/"  # The folder of source DEMs must exist.
PATH_ASTGDEM_REFORM = "DATA/DATA_ASTGDEMv20/EPSG4326_r/"  # The folder of reformed DEMs.

# Set the name of DEMs in GCSs.
ASTGDEM_GCS_WD = "ASTGDEMv20_EPSG4326.tif"
ASTGDEM_GCS_UK = "ASTGDEMv20_EPSG4277.tif"
ASTGDEM_GCS_EU = "ASTGDEMv20_EPSG4258.tif"

# Set the name of DEMs in PCSs.
ASTGDEM_PCS_WD = "ASTGDEMv20_EPSG3857.tif"
ASTGDEM_PCS_UK = "ASTGDEMv20_EPSG27700.tif"
ASTGDEM_PCS_EU = "ASTGDEMv20_EPSG3035.tif"

# Set the path for saving 2D DEM images.
IMG_PATH_ASTGDEM = "IMG_ASTGDEMv20/"

# Set the name of 2D DEM images.
IMG_NAME_ASTGDEM_WD = "LD_ASTGDEMv20_EPSG3857"
IMG_NAME_ASTGDEM_UK = "LD_ASTGDEMv20_EPSG27700"
IMG_NAME_ASTGDEM_EU = "LD_ASTGDEMv20_EPSG3035"

# Set the path of location data file.
PATH_LD_STATION_DATA = "DATA/DATA_LD_AirQuality/London_AirQuality_Stations.csv"


# In[3]:


# <ASTGDEMv20> Remove the overlapped elements of DEMs in WGS-84 GCS.

print('\n>>> <ASTGDEMv20> Remove the overlapped elements of DEMs in WGS-84 GCS.')

file_names = get_file_names(PATH_ASTGDEM_SOURCE, DEM_FORMAT)
file_names.sort(reverse=True)  # W -> E

for i, file_name in enumerate(file_names):
    print('\n>>> Process the %d-th DEM: %s' % (i + 1, file_name))

    gdal_data = gdal.Open(PATH_ASTGDEM_SOURCE + file_name)
    i_row, i_col, i_band, i_gt, i_proj = get_dem_info(gdal_data, 1)
    print('\n*==> The shape of DEM is: [%d, %d]' % (i_row, i_col))

    gdal_array = gdal_data.ReadAsArray().astype(np.float)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    if np.any(gdal_array == nodataval):
        gdal_array[gdal_array == nodataval] = np.nan

    # Remove the overlapped elements of DEM.
    dem_reform = gdal_array
    dem_reform = np.delete(dem_reform, -1, axis=0)  # Delete the last/bottom row of DEM.
    dem_reform = np.delete(dem_reform, -1, axis=1)  # Delete the last/right column of DEM.
    print('\n*==> The shape of the reformed DEM is: [%d, %d]' % (dem_reform.shape[0], dem_reform.shape[1]))

    print('\n>>> Write the reformed DEM to:', file_name)
    path = PATH_ASTGDEM_REFORM
    if os.path.exists(path) is False:
        os.mkdir(path)
    if os.path.isfile(path + file_name) is True:
        os.remove(path + file_name)
    write_dem(path + file_name, dem_reform, dem_reform.shape[0], dem_reform.shape[1], i_band, i_gt, i_proj)

print('\n>>> Complete!\n')


# In[4]:


# <ASTGDEMv20> Merge the reformed DEMs in WGS-84 GCS.

print('\n>>> <ASTGDEMv20> Merge the reformed DEMs in WGS-84 GCS.')

dem_merge = []
dem_out = ASTGDEM_GCS_WD

file_names = get_file_names(PATH_ASTGDEM_REFORM, DEM_FORMAT)
file_names.sort(reverse=True)  # W -> E

for i, file_name in enumerate(file_names):
    if 'ASTGTM2' in file_name:
        print('\n>>> Read the %d-th DEM: %s' % (i + 1, file_name))

        gdal_data = gdal.Open(PATH_ASTGDEM_REFORM + file_name)
        i_row, i_col, i_band, i_gt, i_proj = get_dem_info(gdal_data, 1)
        print('\n*==> The shape of DEM is: [%d, %d]' % (i_row, i_col))

        gdal_array = gdal_data.ReadAsArray().astype(np.float)
        gdal_band = gdal_data.GetRasterBand(1)
        nodataval = gdal_band.GetNoDataValue()
        if np.any(gdal_array == nodataval):
            gdal_array[gdal_array == nodataval] = np.nan

        # Merge the reformed DEMs. - Not perfect.
        name_lat = re.findall(r'-?\d+\.?\d*', file_name)[1]
        name_log = re.findall(r'-?\d+\.?\d*', file_name)[2]

        if name_lat == '51':
            if name_log == '001':
                dem_merge = gdal_array
            else:
                dem_merge = np.concatenate((dem_merge, gdal_array), axis=1)

print('\n*==> The shape of the merged DEM is: [%d, %d]' % (dem_merge.shape[0], dem_merge.shape[1]))

# Get the GeoTransform parameters of the merged DEM from the left-top DEM ('file_names[0]').
gdal_data = gdal.Open(PATH_ASTGDEM_REFORM + file_names[0])
lt_row, lt_col, lt_band, lt_gt, lt_proj = get_dem_info(gdal_data)

print('\n>>> Write the merged DEM to:', dem_out)
path = PATH_ASTGDEM
if os.path.exists(path) is False:
    os.mkdir(path)
if os.path.isfile(path + dem_out) is True:
        os.remove(path + dem_out)
write_dem(path + dem_out, dem_merge, dem_merge.shape[0], dem_merge.shape[1], lt_band, lt_gt, lt_proj)

print('\n>>> Complete!\n')


# In[5]:


# <ASTGDEMv20> Transform the merged DEM from WGS-84 GCS to OSGB-36 GCS.

print('\n>>> <ASTGDEMv20> Transform the merged DEM from WGS-84 GCS to OSGB-36 GCS.')

path = PATH_ASTGDEM
dem_in = path + ASTGDEM_GCS_WD
dem_out = path + ASTGDEM_GCS_UK

epsg_in = 4326
epsg_out = 4277

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# In[6]:


# <ASTGDEMv20> Transform the merged DEM from WGS-84 GCS to ETRS-89 GCS.

print('\n>>> <ASTGDEMv20> Transform the merged DEM from WGS-84 GCS to ETRS-89 GCS.')

path = PATH_ASTGDEM
dem_in = path + ASTGDEM_GCS_WD
dem_out = path + ASTGDEM_GCS_EU

epsg_in = 4326
epsg_out = 4258

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# In[7]:


# <ASTGDEMv20> Project DEM from WGS-84 GCS to Pseudo Mercator PCS.

print('\n>>> <ASTGDEMv20> Project DEM from WGS-84 GCS to Pseudo Mercator PCS.')

path = PATH_ASTGDEM
dem_in = path + ASTGDEM_GCS_WD
dem_out = path + ASTGDEM_PCS_WD

epsg_in = 4326
epsg_out = 3857

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# In[8]:


# <ASTGDEMv20> Project DEM from OSGB-36 GCS to BNG PCS.

print('\n>>> <ASTGDEMv20> Project DEM from OSGB-36 GCS to BNG PCS.')

path = PATH_ASTGDEM
dem_in = path + ASTGDEM_GCS_UK
dem_out = path + ASTGDEM_PCS_UK

epsg_in = 4277
epsg_out = 27700

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# In[9]:


# <ASTGDEMv20> Project DEM from ETRS-89 GCS to LAEA PCS.

print('\n>>> <ASTGDEMv20> Project DEM from ETRS-89 GCS to LAEA PCS.')

path = PATH_ASTGDEM
dem_in = path + ASTGDEM_GCS_EU
dem_out = path + ASTGDEM_PCS_EU

epsg_in = 4258
epsg_out = 3035

transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out)

data = gdal.Open(dem_in)
get_dem_info(data, 1)
data = gdal.Open(dem_out)
get_dem_info(data, 1)

print('\n>>> Complete!\n')


# In[10]:


# <ASTGDEMv20> Display DEM in PCS as a 2D image.

dem_path = PATH_ASTGDEM
img_path = IMG_PATH_ASTGDEM

# Create the path for saving 2D DEM images.
if os.path.exists(img_path) is False:
    os.mkdir(img_path)

# Display 2D DEM image in Pseudo Mercator PCS.
print('\n>>> <ASTGDEMv20> Display 2D DEM image in Pseudo Mercator PCS.')
dem_name = ASTGDEM_PCS_WD
img_name = IMG_NAME_ASTGDEM_WD
# show_2d_dem(dem_path, dem_name, img_path, img_name)

# Display 2D DEM image in BNG PCS.
print('\n>>> <ASTGDEMv20> Display 2D DEM image in BNG PCS.')
dem_name = ASTGDEM_PCS_UK
img_name = IMG_NAME_ASTGDEM_UK
# show_2d_dem(dem_path, dem_name, img_path, img_name)

# Display 2D DEM image in LAEA PCS.
print('\n>>> <ASTGDEMv20> Display 2D DEM image in LAEA PCS.')
dem_name = ASTGDEM_PCS_EU
img_name = IMG_NAME_ASTGDEM_EU
# show_2d_dem(dem_path, dem_name, img_path, img_name)

print('\n>>> Complete!\n')


# In[11]:


# Read London air quality monitoring station data file.

print('\n>>> Read London air quality monitoring station data file.')

site_data = read_csv(PATH_LD_STATION_DATA)
print(site_data.head(3))

site_num = site_data['SiteName'].count()
print('\n*==> The number of stations is: %d' % site_num)

# Get the latitude and longitude of stations.
site_latlng = np.zeros((site_num, 2))
site_latlng[:, 0] = site_data['Latitude']  # 0-th column - Latitude.
site_latlng[:, 1] = site_data['Longitude']  # 1-th column - Longitude.

np.set_printoptions(suppress=True)  # Print numbers without scientific notation.
print('\n*==> The location (lat, lng) of stations are:\n', site_latlng)

print('\n>>> Complete!\n')


# In[12]:


# <ASTGDEMv20> Get the elevation from DEM in WGS-84 GCS.

print('\n>>> <ASTGDEMv20> Get the elevation from DEM in WGS-84 GCS.')

dem_gcs = gdal.Open(PATH_ASTGDEM + ASTGDEM_GCS_WD)
get_dem_info(dem_gcs, 1)

site_ele_astgdem_wgs = get_elevation(dem_gcs, site_latlng)
np.set_printoptions(suppress=True)

print('\n*==> The elevation information of stations is:\n', site_ele_astgdem_wgs)
print('\n*==> The elevation value of stations is:\n', site_ele_astgdem_wgs[:, 5].astype(int))

print('\n>>> Complete!\n')


# In[13]:


# <ASTGDEMv20> Get the elevation from DEM in OSGB-36 GCS.

print('\n>>> <ASTGDEMv20> Get the elevation from DEM in OSGB-36 GCS.')

dem_gcs = gdal.Open(PATH_ASTGDEM + ASTGDEM_GCS_UK)
get_dem_info(dem_gcs, 1)

site_ele_astgdem_osgb = get_elevation(dem_gcs, site_latlng)
np.set_printoptions(suppress=True)

print('\n*==> The elevation information of stations is:\n', site_ele_astgdem_osgb)
print('\n*==> The elevation value of stations is:\n', site_ele_astgdem_osgb[:, 5].astype(int))

print('\n>>> Complete!\n')


# In[14]:


# <ASTGDEMv20> Get the elevation from DEM in ETRS-89 GCS.

print('\n>>> <ASTGDEMv20> Get the elevation from DEM in ETRS-89 GCS.')

dem_gcs = gdal.Open(PATH_ASTGDEM + ASTGDEM_GCS_EU)
get_dem_info(dem_gcs, 1)

site_ele_astgdem_etrs = get_elevation(dem_gcs, site_latlng)
np.set_printoptions(suppress=True)

print('\n*==> The elevation information of stations is:\n', site_ele_astgdem_etrs)
print('\n*==> The elevation value of stations is:\n', site_ele_astgdem_etrs[:, 5].astype(int))

print('\n>>> Complete!\n')


# In[15]:


# Compare the elevation obtained from different DEMs.

print('\n>>> Compare the elevation obtained from different DEMs.')

print('\nASTGDEMv20_WD', site_ele_astgdem_wgs[:, 5].astype(int))
print('\nASTGDEMv20_UK', site_ele_astgdem_osgb[:, 5].astype(int))
print('\nASTGDEMv20_EU', site_ele_astgdem_etrs[:, 5].astype(int))

print('\n>>> Complete!\n')
