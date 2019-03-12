### Function: Process Digital Elevation Models (DEMs) with Python.

# Written by He Zhang, University of Exeter
# Date: Feb 11th 2019 (Revised Mar 12th 2019)
# Contact: hz298@exeter.ac.uk

# DEM Data:
#     - ASTER GDEM v2.0 (ASTGDEM-v2.0)
#     Download Link: https://earthexplorer.usgs.gov/
#     - EU DEM v1.1 (EUDEM-v1.1)
#     Download Link: https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

# Terms and Abbreviations:
#     EPSG     -  European Petroleum Survey Group
#     GCS      -  Geographic Coordinate System
#     PCS      -  Projected Coordinate System
#     WGS-84   -  1984 World Geodetic System [GCS]
#     OSGB-36  -  1936 Ordnance Survey Great Britain [GCS]
#     BNG      -  British National Grid [PCS of OSGB-36]
#     ETRS-89  -  1989 European Terrestrial Reference System [GCS]

# Functions:
#     For ASTGDEM-v2.0:
#         1. Remove overlapped elements of ASTGDEM-v2.0 data in WGS-84 GCS.
#         2. Merge reformed ASTGDEM-v2.0 data in WGS-84 GCS.
#         3. Transform ASTGDEM-v2.0 data from WGS-84 GCS [EPSG-4326] to OSGB-36 GCS [EPSG-4277].
#         4. Project ASTGDEM-v2.0 data from WGS-84 GCS to Web Mercator PCS [EPSG-3857].
#         4. Project ASTGDEM-v2.0 data from OSGB-36 GCS to BNG PCS [EPSG-27700].
#         5. Display ASTGDEM-v2.0 data in PCSs as 2D images (x2).
#         6. Get elevation of air quality stations from ASTGDEM-v2.0 data in WGS-84 GCS.
#         6. Get elevation of air quality stations from ASTGDEM-v2.0 data in OSGB-36 GCS.
#     For EUDEM-v1.1:
#         1. Re-Project EUDEM-v1.1 data from ETRS-LAEA PCS [EPSG-3035] to ETRS-89 GCS [EPSG-4258].
#         2. Get elevation of air quality stations from EUDEM-v1.1 data in ETRS-89 GCS.

# **************************** Important Notice of Code ****************************
#     - Use GDAL.GetProjection() to check the GCS or PCS of DEM in TIF format.
#     - Use GDAL.GetGeoTransform() to check the resolution and the top-left corner location of the map.
#     - You can transform DEM between different GCSs (e.g., WGS-84<->OSGB-36<->ETRS-89).
#     - You can not display DEM in GCS as 2D image (i.e., imshow(DEMinGCS) is wrong).
#     - Each GCS has a related PCS. Project DEM in GCS to the related PCS and then display its 2D image.
#     - You can not project DEM in GCS to the PCS related to another GCS (e.g., WGS-84->BNG is wrong).


import os
import shutil
from osgeo import gdal
import numpy as np
import re
import subprocess
import matplotlib.pyplot as plt
from pandas import read_csv


def get_FileName(file_path, file_type):
    files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    
    file_names = []
    for i in files:
        if file_type in i:
            file_names.append(i)
    
    return file_names


def get_TifInfo(dem_data, tag_print):
    dem_row = dem_data.RasterYSize  # Height.
    dem_col = dem_data.RasterXSize  # Width.
    dem_band = dem_data.RasterCount
    dem_geotran = dem_data.GetGeoTransform()
    dem_proj = dem_data.GetProjection()
    
    if tag_print == 1:
        print('\n==> DEM data information:')
        print('===> The number of rows of DEM array is: %d (height).' % dem_row)
        print('===> The number of cols of DEM array is: %d (width).' % dem_col)
        print('===> The number of bands of DEM array is: %d.' % dem_band)
        print('===> The 6 GeoTransform parameters of DEM data is:')
        print(dem_geotran)
        print('===> The projection information of DEM data is:')
        print(dem_proj)
    
    return dem_row, dem_col, dem_band, dem_geotran, dem_proj


def write_TIF(dem_array, dem_row, dem_col, dem_band, dem_geotran, dem_proj, path):
    data_type = gdal.GDT_UInt16  # This should be changed for different DEM files.
    
    if len(dem_array.shape) == 3:
        dem_band, dem_row, dem_col = dem_array.shape
    elif len(dem_array.shape) == 2:
        dem_array = np.array([dem_array])
    else:
        dem_band, (dem_row, dem_col) = 1, dem_array.shape
    
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, dem_col, dem_row, dem_band, data_type)  # col -> row.
    if(dataset is not None):
        dataset.SetGeoTransform(dem_geotran)
        dataset.SetProjection(dem_proj)
    for i in range(dem_band):
        dataset.GetRasterBand(i + 1).WriteArray(dem_array[i])
    del dataset
    
    return 0


def show_ProjDEM(file_path, file_name, img_path, img_name):
    gdal_data = gdal.Open(file_path + file_name)

    gdal_array = gdal_data.ReadAsArray().astype(np.float)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    if np.any(gdal_array == nodataval):
        gdal_array[gdal_array == nodataval] = np.nan
    print('\n*==> The shape of the DEM array is: [%d, %d].' % (gdal_array.shape[0], gdal_array.shape[1]))
    
    print('>>>> Plot DEM image.')
    fig = plt.figure(figsize=(5, 10))
    plt.title('2D Image of ' + img_name)
    plt.imshow(gdal_array)
    plt.show()
    
    save_path = img_path
    if os.path.exists(save_path) is False:  # Check if the path/folder exists.
            os.mkdir(save_path)  # Create the path/folder.
    fig.savefig(save_path + img_name + '.png')
    
    return 0


def get_Elevation(gcs_data, site_latlog):
    gt = gcs_data.GetGeoTransform()
    print('\n*==> The GeoTransform parameters are:\n', gt)
    
    gcs_array = gcs_data.ReadAsArray().astype(np.float)
    gcs_band = gcs_data.GetRasterBand(1)
    nodataval = gcs_band.GetNoDataValue()
    if np.any(gcs_array == nodataval):
        gcs_array[gcs_array == nodataval] = np.nan
    
    M = site_latlog.shape[0]
    Xgeo = site_latlog[:, 1]  # Longitude.
    Ygeo = site_latlog[:, 0]  # Latitude.
    
    ele = np.zeros((M, 6))  # The elevation of M locations.
    for i in range(M):
        # Note:
        #     Xgeo = GT[0] + Xpixel*GT[1] + Yline*GT[2]
        #     Ygeo = GT[3] + Xpixel*GT[4] + Yline*GT[5]
        #
        #     Xpixel - Pixel/column of 2D DEM image
        #     Yline - Line/row of 2D DEM image
        #
        #     Xgeo - Longitude
        #     Ygeo - Latitude
        #
        #     [0] = Longitude of left-top pixel
        #     [3] = Latitude of left-top pixel
        #
        #     [1] = + Pixel width
        #     [5] = - Pixel height
        #
        #     [2] = 0 for north up image
        #     [4] = 0 for north up image
        
        Xpixel = int(round((Xgeo[i] - gt[0]) / gt[1]))
        Yline = int(round((Ygeo[i] - gt[3]) / gt[5]))
        
        ele[i, 0] = int(i)  # i-th location.
        ele[i, 1] = Ygeo[i]  # Latitude.
        ele[i, 2] = Xgeo[i]  # Longitude.
        ele[i, 3] = Yline  # Row.
        ele[i, 4] = Xpixel  # Column.
        ele[i, 5] = gcs_array[Yline, Xpixel]  # The elevation of i-th location.
    
    return ele


## Specify the type and path of DEM files.

file_type = ".tif"

# _s - Source data files.
# _r - Reformed data files.

path_astgdem_source = "DATA/DATA_ASTGDEMv20/EPSG4326_s/"
path_astgdem_reform = "DATA/DATA_ASTGDEMv20/EPSG4326_r/"
path_astgdem = "DATA/DATA_ASTGDEMv20/"

path_eudem_source = "DATA/DATA_EUDEMv11/EPSG3035_s/"
path_eudem = "DATA/DATA_EUDEMv11/"


## <ASTGDEM-v2.0> Remove overlapped elements of ASTGDEM-v2.0 data in WGS-84 GCS.

print('\n>>> ******************** ASTGDEM-v2.0 ********************')

print('\n>>> Start removing overlapped elements of ASTGDEM-v2.0 data in WGS-84 GCS.')

file_names = get_FileName(path_astgdem_source, file_type)
file_names.sort(reverse=True)  # W -> E.
for i, name in enumerate(file_names):
    print('\n>>> Process the %d-th DEM file: %s.' % (i + 1, name))
    
    gdal_data = gdal.Open(path_astgdem_source + name)
    tag = 1  # Do print info.
    row, col, band, geotran, proj = get_TifInfo(gdal_data, tag)
    gdal_array = gdal_data.ReadAsArray().astype(np.float)
    print('\n*==> The shape of DEM array is: [%d, %d].' % (gdal_array.shape[0], gdal_array.shape[1]))
    
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    if np.any(gdal_array == nodataval):
        gdal_array[gdal_array == nodataval] = np.nan
    
    gdal_array = np.delete(gdal_array, -1, axis=0)  # Delete Last/Bottom Row.
    gdal_array = np.delete(gdal_array, -1, axis=1)  # Delete Last/Right Col.
    print('*==> The shape of reformed DEM array is: [%d, %d].' % (gdal_array.shape[0], gdal_array.shape[1]))
    
    path = path_astgdem_reform
    if os.path.exists(path) is False:
        os.mkdir(path)
    tmp_path = path + name  # Set the path with folder name and file name.
    print('\n>>> Write reformed DEM data to TIF file.')
    write_TIF(gdal_array, gdal_array.shape[0], gdal_array.shape[1], band, geotran, proj, tmp_path)

print('\n>>> Complete!\n')


## <ASTGDEM-v2.0> Merge reformed ASTGDEM-v2.0 data in WGS-84 GCS.

print('\n>>> Start merging reformed ASTGDEM-v2.0 data in WGS-84 GCS.')

dem_out = "ASTGDEMv20_EPSG4326.tif"

file_names = get_FileName(path_astgdem_reform, file_type)
file_names.sort(reverse=True)  # W -> E.
dem_merged_array = []
for i, name in enumerate(file_names):
    if "ASTGTM2" in name:  # Select ASTGTM2_***.tif files.
        print('\n>>> Read the %d-th DEM file: %s.' % (i + 1, name))

        gdal_data = gdal.Open(path_astgdem_reform + name)
        gdal_array = gdal_data.ReadAsArray().astype(np.float)
        print('*==> The shape of DEM array is: [%d, %d].' % (gdal_array.shape[0], gdal_array.shape[1]))

        gdal_band = gdal_data.GetRasterBand(1)
        nodataval = gdal_band.GetNoDataValue()
        if np.any(gdal_array == nodataval):
            gdal_array[gdal_array == nodataval] = np.nan

        # Merge DEM arrays.
        tmp = re.findall(r'-?\d+\.?\d*', name)
        tmp_Lat = tmp[1]
        tmp_Log = tmp[2]
        if tmp_Lat == '51':  # not perfect.
            if tmp_Log == '001':
                dem_merged_array = gdal_array
            else:
                dem_merged_array = np.concatenate((dem_merged_array, gdal_array), axis=1)

print('\n*==> The shape of merged DEM array is: [%d, %d].' % (dem_merged_array.shape[0], dem_merged_array.shape[1]))

# Set the correct GeoTransform parameters (according to the left-top DEM file).
gdal_data = gdal.Open(path_astgdem_reform + file_names[0])
tag = 0  # Not print info.
row, col, band, geotran, proj = get_TifInfo(gdal_data, tag)

path = path_astgdem
if os.path.exists(path) is False:
    os.mkdir(path)
tmp_path = path + dem_out  # Set the path with folder name and file name.
print('\n>>> Write merged DEM data to ' + dem_out)
write_TIF(dem_merged_array, dem_merged_array.shape[0], dem_merged_array.shape[1], band, geotran, proj, tmp_path)

print('\n>>> Complete!\n')


## <ASTGDEM-v2.0> Transform ASTGDEM-v2.0 data from WGS-84 GCS [EPSG-4326] to OSGB-36 GCS [EPSG-4277].

print('\n>>> Start transforming ASTGDEM-v2.0 data from WGS-84 GCS [EPSG-4326] to OSGB-36 GCS [EPSG-4277].\n')

path = path_astgdem
dem_in = path + "ASTGDEMv20_EPSG4326.tif"
dem_out = path + "ASTGDEMv20_EPSG4277.tif"

# Check if the output file exists. If so, delete it.
if os.path.isfile(dem_out) is True:
    os.remove(dem_out)

command = "gdalwarp -s_srs EPSG:4326 -t_srs EPSG:4277" + " " + dem_in + " " + dem_out  # Change EPSG Code.

subprocess.call(command, shell=True)

print('\n>>> Complete!\n')


## <ASTGDEM-v2.0> Project ASTGDEM-v2.0 data from WGS-84 GCS to Web Mercator PCS [EPSG-3857].

print('\n>>> Start projecting ASTGDEM-v2.0 data from WGS-84 GCS to Web Mercator PCS [EPSG-3857].\n')

path = path_astgdem
dem_in = path + "ASTGDEMv20_EPSG4326.tif"
dem_out = path + "ASTGDEMv20_EPSG3857.tif"

# Check if the output file exists. If so, delete it.
if os.path.isfile(dem_out) is True:
    os.remove(dem_out)

command = "gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3857" + " " + dem_in + " " + dem_out  # Change EPSG Code.

subprocess.call(command, shell=True)

print('\n>>> Complete!\n')


## <ASTGDEM-v2.0> Project ASTGDEM-v2.0 data from OSGB-36 GCS to BNG PCS [EPSG-27700].

print('\n>>> Start projecting ASTGDEM-v2.0 data from OSGB-36 GCS to BNG PCS [EPSG-27700].\n')

path = path_astgdem
dem_in = path + "ASTGDEMv20_EPSG4277.tif"
dem_out = path + "ASTGDEMv20_EPSG27700.tif"

# Check if the output file exists. If so, delete it.
if os.path.isfile(dem_out) is True:
    os.remove(dem_out)

command = "gdalwarp -s_srs EPSG:4277 -t_srs EPSG:27700" + " " + dem_in + " " + dem_out  # Change EPSG Code.

subprocess.call(command, shell=True)

print('\n>>> Complete!\n')


## <ASTGDEM-v2.0> Display ASTGDEM-v2.0 data in PCSs as 2D images (x2).

print('\n>>> Start displaying ASTGDEM-v2.0 data in PCSs as 2D images (x2).')

# path = path_astgdem
# img_path = "IMG/"
# if os.path.exists(img_path) is True:  # Check if the path/folder exists.
#     shutil.rmtree(img_path)  # Delete the folder, its child folders and child files.
# os.mkdir(img_path)  # Create a new folder for saving 2D DEM images.

# # DEM in Web Mercator PCS.
# dem_name = "ASTGDEMv20_EPSG3857.tif"
# img_name = "LD_ASTGDEMv20_EPSG3857"
# show_ProjDEM(path, dem_name, img_path, img_name)
# data = gdal.Open(path + dem_name)
# get_TifInfo(data, 1)

# # DEM in BNG PCS.
# dem_name = "ASTGDEMv20_EPSG27700.tif"
# img_name = "LD_ASTGDEMv20_EPSG27700"
# show_ProjDEM(path, dem_name, img_path, img_name)
# data = gdal.Open(path + dem_name)
# get_TifInfo(data, 1)

print('\n>>> Complete!\n')


## <EUDEM-v1.1> Read EUDEM-v1.1 data (~1 minute, not needed).

print('\n>>> ******************** EUDEM-v1.1 ********************')

file_names = get_FileName(path_eudem_source, file_type)
for i, name in enumerate(file_names):
    print('\n>>> Read the %d-th DEM file: %s.' % (i + 1, name))
    
    gdal_data = gdal.Open(path_eudem_source + name)
    tag = 1  # Do print info.
    row, col, band, geotran, proj = get_TifInfo(gdal_data, tag)
    gdal_array = gdal_data.ReadAsArray().astype(np.float)
    print('\n*==> The shape of DEM array is: [%d, %d].' % (gdal_array.shape[0], gdal_array.shape[1]))
    
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    if np.any(gdal_array == nodataval):
        gdal_array[gdal_array == nodataval] = np.nan

print('\n>>> Complete!\n')


## <EUDEM-v1.1> Re-Project EUDEM-v1.1 data from ETRS-LAEA PCS [EPSG-3035] to ETRS-89 GCS [EPSG-4258] (~3 minutes).

print('\n>>> Start re-projecting EUDEM-v1.1 data from ETRS-LAEA PCS [EPSG-3035] to ETRS-89 GCS [EPSG-4258].\n')

path = path_eudem
dem_in = path + "EUDEMv11_EPSG3035.tif"
dem_out = path + "EUDEMv11_EPSG4258.tif"

# Check if the output file exists. If so, delete it.
if os.path.isfile(dem_out) is True:
    os.remove(dem_out)

command = "gdalwarp -s_srs EPSG:3035 -t_srs EPSG:4258" + " " + dem_in + " " + dem_out  # Change EPSG Code.

subprocess.call(command, shell=True)

print('\n>>> Complete!\n')

# It takes a long time to display the whole image of one EUDEM-v1.1 data file.


## Read London air quality monitoring station information.

print('\n>>> Start reading London air quality monitoring station information.\n')

site_path = "DATA/DATA_LD_AirQuality/London_AirQuality_Stations.csv"
site_data_raw = read_csv(site_path)  # Station data <'pandas.DF'>.
print(site_data_raw.head(3))

site_num = site_data_raw['SiteName'].count()  # The number of stations.
print('\n*==> The number of stations is: %d.' % site_num)

site_latlog = np.zeros((site_num, 2))  # The latitude and longitude of stations.
site_latlog[:, 0] = site_data_raw['Latitude']  # 0-th col - latitude.
site_latlog[:, 1] = site_data_raw['Longitude']  # 1-th col - longitude.

np.set_printoptions(suppress=True)  # Print numbers without scientific notation.
print('\n*==> The latitude and longitude of stations are:')
print(site_latlog)

print('\n>>> Complete!\n')


## Specify the name and path of DEM data in GCSs.

gcs_path_astgdem = "DATA/DATA_ASTGDEMv20/"
gcs_wgs = "ASTGDEMv20_EPSG4326.tif"
gcs_osgb = "ASTGDEMv20_EPSG4277.tif"

gcs_path_eudem = "DATA/DATA_EUDEMv11/"
gcs_etrs = "EUDEMv11_EPSG4258.tif"


## <ASTGDEM-v2.0> Get the elevation of stations from ASTGDEM-v2.0 data in WGS-84 GCS.

print('\n>>> Start getting the elevation of stations from ASTGDEM-v2.0 data in WGS-84 GCS.')

gcs_data = gdal.Open(gcs_path_astgdem + gcs_wgs)

tag = 1
get_TifInfo(gcs_data, tag)

# Get elevation.
site_ele_wgs = get_Elevation(gcs_data, site_latlog)
np.set_printoptions(suppress=True)  # Print numbers without scientific notation.

print('\n*==> The detailed elevation of stations is:')
print(site_ele_wgs)
print('\n*==> The summarized elevation of stations is:')
print(site_ele_wgs[:, 5].astype(int))

print('\n>>> Complete!\n')


## <ASTGDEM-v2.0> Get the elevation of stations from ASTGDEM-v2.0 data in OSGB-36 GCS.

print('\n>>> Start getting the elevation of stations from ASTGDEM-v2.0 data in OSGB-36 GCS.')

gcs_data = gdal.Open(gcs_path_astgdem + gcs_osgb)

tag = 1
get_TifInfo(gcs_data, tag)  # Do print info.

# Get elevation.
site_ele_osgb = get_Elevation(gcs_data, site_latlog)
np.set_printoptions(suppress=True)  # Print digital values without scientific notation.

print('\n*==> The detailed elevation of stations is:')
print(site_ele_osgb)
print('\n*==> The summarized elevation of stations is:')
print(site_ele_osgb[:, 5].astype(int))

print('\n>>> Complete!\n')


## <EUDEM-v1.1> Get the elevation of stations from EUDEM-v1.1 data in ETRS-89 GCS (~1 minute).

print('\n>>> Start getting the elevation of stations from EUDEM-v1.1 data in ETRS-89 GCS.')

gcs_data = gdal.Open(gcs_path_eudem + gcs_etrs)

tag = 1
get_TifInfo(gcs_data, tag)

# Get elevation.
site_ele_etrs = get_Elevation(gcs_data, site_latlog)
np.set_printoptions(suppress=True)  # Print numbers without scientific notation.

print('\n*==> The detailed elevation of stations is:')
print(site_ele_etrs)
print('\n*==> The summarized elevation of stations is:')
print(site_ele_etrs[:, 5].astype(int))

print('\n>>> Complete!\n')


print('\n>>> Comparison of elevation from different DEMs and GCSs.\n')

print('WGS-84  ', site_ele_wgs[:, 5].astype(int))  # ASTGDEM-v2.0 data in WGS-84 GCS.

print('OSGB-36 ', site_ele_osgb[:, 5].astype(int))  # ASTGDEM-v2.0 data in OSGB-36 GCS.

print('OSGB-36 ', site_ele_etrs[:, 5].astype(int))  # EUDEM-v1.1 data in ETRS-89 GCS.

print('\n>>> Complete!\n')
