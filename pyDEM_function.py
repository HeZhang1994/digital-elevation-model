import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal


def get_file_names(file_path, file_type):
    '''Get the name of files in specified type in a folder.

    Parameters:
        file_path <str> -- The path of folder.
        file_type <str> -- The type of files.

    Return:
        file_names <list> -- The name of files with extension.
    '''
    file_names = []
    files = [file for file in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, file))]
    for file in files:
        if file_type in file:
            file_names.append(file)

    return file_names


def get_dem_info(dem_data, if_print=False):
    '''Get the information of DEM data.

    Parameters:
        dem_data <osgeo.gdal.Dataset> -- The data of DEM.
        if_print <bool> -- If print the information of DEM. Default is False (not print).

    Return:
        ... <...> -- The information and parameters of DEM.
    '''
    dem_row = dem_data.RasterYSize  # height
    dem_col = dem_data.RasterXSize  # width
    dem_band = dem_data.RasterCount
    dem_gt = dem_data.GetGeoTransform()
    dem_proj = dem_data.GetProjection()

    if if_print:
        print('\nThe information of DEM:')
        print('The number of row (height) is: %d' % dem_row)
        print('The number of column (width) is: %d' % dem_col)
        print('The number of band is: %d' % dem_band)
        print('The 6 GeoTransform parameters are:\n', dem_gt)
        print('The GCS/PCS information is:\n', dem_proj)

    return dem_row, dem_col, dem_band, dem_gt, dem_proj


def write_dem(d_path, d_array, d_row, d_col, d_band, d_gt, d_proj, d_type=gdal.GDT_UInt16, d_frmt='GTiff'):
    '''Write data to a new DEM.

    Parameters:
        d_path <str> -- The path for saving new DEM.
        d_array <numpy.ndarray> -- The data array.
        d_row <int> -- The height of new DEM.
        d_col <int> -- The width of new DEM.
        d_band <int> -- The band number of new DEM.
        d_gt <tuple> -- The 6 GeoTransform parameters of new DEM.
        d_proj <str> -- The GCS/PCS information of new DEM.
        d_type <str> -- The data type of new DEM. Default is gdal.GDT_UInt16.
        d_frmt <str> -- The data format of new DEM. Default is 'GTiff'.

    Return:
        0 <int> -- If writing to new DEM is completed.
    '''
    if len(d_array.shape) == 3:
        d_band, d_row, d_col = d_array.shape
    elif len(d_array.shape) == 2:
        d_array = np.array([d_array])
    else:
        d_band, (d_row, d_col) = 1, d_array.shape

    driver = gdal.GetDriverByName(d_frmt)
    data = driver.Create(d_path, d_col, d_row, d_band, d_type)  # (col, row)
    if(data is not None):
        data.SetGeoTransform(d_gt)
        data.SetProjection(d_proj)
    for i in range(d_band):
        data.GetRasterBand(i + 1).WriteArray(d_array[i])
    del data

    return 0


def show_2d_dem(dem_path, dem_name, img_path, img_name, img_frmt='.png', img_dpi=100):
    '''Display and save 2D DEM image.

    Parameters:
        dem_path <str> -- The path of DEM (in PCS) for display.
        dem_name <str> -- The name of DEM (with extension).
        img_path <str> -- The path for saving image.
        img_name <str> -- The name of image.
        img_frmt <str> -- The format of image. Default is '.png'.
        img_dpi <int> -- The resolution of image. Default is 100.

    Return:
        0 <int> -- If display and saving image are completed.
    '''
    gdal_data = gdal.Open(dem_path + dem_name)
    gdal_array = gdal_data.ReadAsArray().astype(np.float)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    if np.any(gdal_array == nodataval):
        gdal_array[gdal_array == nodataval] = np.nan
    print('\nThe shape of DEM is: [%d, %d]' % (gdal_array.shape[0], gdal_array.shape[1]))

    # Create the path for saving 2D DEM image.
    if os.path.exists(img_path) is False:
            os.mkdir(img_path)

    fig = plt.figure(dpi=img_dpi)
    plt.title('2D DEM Image of ' + img_name)
    plt.imshow(gdal_array)
    plt.show()
    fig.savefig(img_path + img_name + img_frmt)

    return 0


def get_elevation(dem_gcs, site_latlng):
    '''Get the elevation of given locations from DEM in GCS.

    Parameters:
        dem_gcs <osgeo.gdal.Dataset> -- The input DEM (in GCS).
        site_latlng <numpy.ndarray> -- The latitude and longitude of given locations.

    Return:
        site_ele <numpy.ndarray> -- The elevation and other information of given locations.
    '''
    gdal_data = dem_gcs
    gdal_array = gdal_data.ReadAsArray().astype(np.float)
    gdal_band = gdal_data.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()
    if np.any(gdal_array == nodataval):
        gdal_array[gdal_array == nodataval] = np.nan

    gt = gdal_data.GetGeoTransform()
    print('\nThe 6 GeoTransform parameters of DEM are:\n', gt)

    N_site = site_latlng.shape[0]
    Xgeo = site_latlng[:, 1]  # longitude
    Ygeo = site_latlng[:, 0]  # latitude

    site_ele = np.zeros((N_site, 6))
    for i in range(N_site):
        # Note:
        #     Xgeo = gt[0] + Xpixel * gt[1] + Yline * gt[2]
        #     Ygeo = gt[3] + Xpixel * gt[4] + Yline * gt[5]
        #
        #     Xpixel - Pixel/column of DEM
        #     Yline - Line/row of DEM
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
        #     [2] = 0 for north up DEM
        #     [4] = 0 for north up DEM

        Xpixel = int(round((Xgeo[i] - gt[0]) / gt[1]))
        Yline = int(round((Ygeo[i] - gt[3]) / gt[5]))

        site_ele[i, 0] = int(i)  # The serial number of i-th location.
        site_ele[i, 1] = Ygeo[i]  # latitude
        site_ele[i, 2] = Xgeo[i]  # longitude
        site_ele[i, 3] = Yline  # cow
        site_ele[i, 4] = Xpixel  # column
        site_ele[i, 5] = gdal_array[Yline, Xpixel]  # The elevation of i-th location.

    return site_ele


def transprojcnvt_dem(dem_in, epsg_in, dem_out, epsg_out):
    '''Transform, project, or convert the coordinate system of DEM.

    Parameters:
        dem_in <str>   -- The path of input DEM.
        epsg_in <int>  -- The EPSG code of input DEM.
        dem_out <str>  -- The path of output DEM.
        epsg_out <int> -- The EPSG code of output DEM.

    Return:
        0 <int> -- If transformation, projection, or conversion is completed.
    '''
    # Check if the output file exists. If so, delete it for overwriting.
    if os.path.isfile(dem_out) is True:
        os.remove(dem_out)

    cmd = 'gdalwarp -s_srs EPSG:' + str(epsg_in) + ' -t_srs EPSG:' + str(epsg_out) + ' ' + dem_in + ' ' + dem_out
    subprocess.call(cmd, shell=True)

    return 0
