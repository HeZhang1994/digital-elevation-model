# Python for Digital Elevation Models (DEMs)

[![image](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![image](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This is a **Python** implementation of transforming, projecting, and visualizing **Digital Elevation Models (DEMs)** (**ASTER-GDEMv2.0** ~30m and **EU-DEMv1.1** ~25m) as well as reading elevation of given locations in London.

## Important Terms and Abbreviations

| Term                                       | Abbreviation | Remark 
| ------------------------------------------ | ------------ | ------ 
| Digital Elevation Model                    | DEM          | - 
| Geographic Coordinate System               | GCS          | [Longitude, Latitude, Elevation] on 3D ellipsoid 
| Projected Coordinate System                | PCS          | [X-axis, Y-axis, Elevation] on 2D plane 
| Georeferenced Tagged Image File Format     | GeoTIFF      | DEM image/data format (.tif) 
| European Petroleum Survey Group            | EPSG         | EPSG codes identify different GCSs and PCSs 
| 1984 World Geodetic System                 | WGS-84       | GCS, EPSG-4326, approx. the ellipsoid of Earth 
| Web Mercator or Pseudo Mercator            | -            | PCS of WGS-84, EPSG-3857 
| 1936 Ordnance Survey Great Britain         | OSGB-36      | GCS, EPSG-4277, approx. the ellipsoid of Britain 
| British National Grid                      | BNG          | PCS of OSGB-36, EPSG-27700 
| 1989 European Terrestrial Reference System | ETRS-89      | GCS, EPSG-4258, approx. the ellipsoid of Europe 

## Functions

- **Transforming** DEM from GCS (e.g., WGS-84) to another GCS (e.g., OSGB-36).

- **Projecting** DEM from GCS (e.g., WGS-84/OSGB-36) to the related PCS (e.g., Web Mercator/BNG).

- **Re-projecting** DEM from PCS (e.g., ETRS-LAEA) to the related GCS (e.g., ETRS-89).

- **Visualizing** DEMs in different PCSs as 2D images.

- **Reading** elevation of specific locations from different DEMs in different GCSs.

## Data

- **ASTER-GDEMv2.0**

Download Link: https://earthexplorer.usgs.gov/

See [Introduction of ASTGDEMv2.pdf](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/Introduction%20of%20ASTGDEMv2.pdf) for details (highly recommended for tyro).

- **EU-DEMv1.1**

Download Link: https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

## Dependencies

* __matplotlib 3.0.2__
* __numpy 1.15.4__
* __gdal (osgeo) 1.11.3__
* __pandas 0.23.4__

The following procedures for installing **GDAL** are partly recapitulated from [mothergeo](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html).

1. Install GDAL Development Libraries and export environment variables for the compiler in Terminal.
```bash
$ sudo apt-get install libgdal-dev

$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal
```

2. Install GDAL Python Libraries in Terminal.
```bash
$ pip install GDAL
```

If it comes with the *error*: ```cpl_vsi_error.h: No such file or directory```, try the following procedures.

3. Check the required/installed version of GDAL Python Libraries in Terminal.
```bash
$ gdal-config --version
```

4. Download the source file (e.g., ```gdal-1.11.3.tar.gz```) of the related GDAL version (e.g., 1.11.3) from [here](http://trac.osgeo.org/gdal/wiki/DownloadSource).

5. Manually install GDAL Python Libraries in Terminal.
```bash
$ cd path/of/downloaded/gdal/package

~$ tar -xvzf gdal-version.tar.gz
# E.g., tar -xvzf gdal-1.11.3.tar.gz

~$ cd extracted/gdal/folder
# E.g., cd gdal-1.11.3

~$ cd swig
~$ cd python
# The setup.py exists in this directory.

~$ python setup.py build_ext --include-dirs=/usr/include/gdal/
~$ python setup.py install
```

6. Try ```>>> from osgeo import gdal``` in Python. If no error occurs, the installation is completed.

## Pipeline

The flow chart of processing London DEM (ASTER-GDEMv2.0). Pictures of Earth are downloaded from [ThoughtCo.](https://www.thoughtco.com/degree-of-latitude-and-longitude-distance-4070616) and [Google Earth](https://earth.google.com/web/).

<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv2_Process_Pipeline.png" height="700">

## Usage

To visualize and read the elevation in London:

1. Prepare ASTER-GDEMv2.0 DEMs.

   1. Download ASTER-GDEMv2.0 DEMs ```ASTGTM2_N51W001_dem.tif``` and ```ASTGTM2_N51E000_dem.tif```.

   2. Copy ASTER-GDEMv2.0 DEMS to ```DATA/DATA_ASTGDEMv20/EPSG4326_s/``` folder.

2. Prepare EU-DEMv1.1 DEM.

   1. Download EU-DEMv1.1 DEM ```eu_dem_v11_E30N30.tif```.

   2. Copy EU-DEMv1.1 DEM to ```DATA/DATA_EUDEMv11/EPSG3035_s/``` folder.

   3. Copy ```eu_dem_v11_E30N30.tif``` to ```DATA/DATA_EUDEMv11/``` folder and rename as ```EUDEMv11_EPSG3035.tif```.

The directory of DEMs is shown in the following figure.

<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/DEM_Data_Contents.png" height="350">

3. Run ```run_PyDEM_London.py``` or ```run_PyDEM_London.ipynb``` (see code comments for details).

## Results

- **London DEM (ASTER-GDEMv2.0) in Web Mercator PCS [EPSG-3857]**

![](https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/LD_EPSG3857.png)

- **London DEM (ASTER-GDEMv2.0) in BNG PCS [EPSG-27700]**

![](https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/LD_EPSG27700.png)

- **Elevation of 5 Locations in London**

| No. | Latitude | Longitude | Elev. in WGS-84 (m)     | Elev. in OSGB-36 (m)     | Elev. in Google Earth (m) 
| --- | -------- | --------- | ----------------------- | ------------------------ | ----------------------------- 
| 1   | 51.52104 | -0.21349  | 31 (+7)                 | 22 (-1)                  | 23 
| 2   | 51.52770 | -0.12905  | 40 (+0)                 | 25 (-15)                 | 40 (Building/Road) 
| 3   | 51.42525 | -0.34560  | 24 (+12)                | 14 (+2)                  | 12 
| 4   | 51.45635 | 0.040725  | 41 (+13)                | 25 (-3)                  | 28 
| 5   | 51.45258 | 0.070766  | 79 (+14)                | 68 (+3)                  | 65 

## References (Highly Recommended for Tyro)

[1] [EPSG 4326 vs EPSG 3857 (projections, datums, coordinate systems, and more!)](http://lyzidiamond.com/posts/4326-vs-3857)

[2] [Coordinate systems and projections for beginners](https://communityhub.esriuk.com/geoxchange/2012/3/26/coordinate-systems-and-projections-for-beginners.html)

[3] [CSDN Blog](https://blog.csdn.net/liuhailiuhai12/article/details/75007417)

<br>

<i>Please star this repository if you found its content useful. Thank you very much.</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。</i>

<i>Last updated: 16/03/2019</i>

