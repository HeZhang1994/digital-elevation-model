# Python for Digital Elevation Models (DEMs)

[![image](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()
[![image](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()
[![image](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This is a **Python** implementation of transforming, projecting, converting and visualizing **Digital Elevation Models** (**ASTERGDEMv2.0** ~30m and **EUDEMv1.1** ~25m) as well as reading elevation of given locations.

## Table of Contents

- [Terms and Abbreviations](#terms-and-abbreviations)
- [Functions](#functions)
- [DEM Data](#dem-data)
  - [ASTERGDEM](#astergdem)
  - [EUDEM](#eudem)
- [Dependencies](#dependencies)
- [Pipeline](#pipeline)
- [Usage](#usage)
- [Results](#results)
- [References](#references)

## Terms and Abbreviations

| Term                                       | Abbreviation | Remark 
| ------------------------------------------ | ------------ | ------ 
| Digital Elevation Model                    | DEM          | - 
| Geographic Coordinate System               | GCS          | [Longitude, Latitude, Elevation] on 3D ellipsoid 
| Projected Coordinate System                | PCS          | [X-coor, Y-coor, Elevation] on 2D plane 
| Georeferenced Tagged Image File Format     | GeoTIFF      | Data Format of DEM (e.g., .tif) 
| European Petroleum Survey Group            | EPSG         | EPSG codes identify different GCSs and PCSs 
| 1984 World Geodetic System                 | WGS-84       | **GCS**, *EPSG-4326*, approx. the ellipsoid of Earth 
| Pseudo Mercator (Web Mercator)             | -            | **PCS** of WGS-84, *EPSG-3857* 
| 1936 Ordnance Survey Great Britain         | OSGB-36      | **GCS**, *EPSG-4277*, approx. the ellipsoid of Britain 
| British National Grid                      | BNG          | **PCS** of OSGB-36, *EPSG-27700* 
| 1989 European Terrestrial Reference System | ETRS-89      | **GCS**, *EPSG-4258*, approx. the ellipsoid of Europe 
| Lambert Azimuthal Equal-Area               | LAEA         | **PCS** of ETRS-89, *EPSG-3035* 

## Functions

- **Transforming** DEM from one GCS (e.g., WGS-84) to another GCS (e.g., OSGB-36).

- **Projecting** DEM from one GCS (e.g., WGS-84/OSGB-36) to the related PCS (e.g., Pseudo Mercator/BNG).

- **Converting** DEM from one PCS (e.g., LAEA) to the related GCS (e.g., ETRS-89).

- **Visualizing** DEM in PCS as a 2D image.

- **Reading** elevation of given locations from DEM in GCS.

## DEM Data

### ASTERGDEM

ASTERGDEMv2.0 Download Link: https://earthexplorer.usgs.gov/

See [Introduction of ASTGDEMv2.pdf](https://github.com/HeZhang1994/digital-elevation-model/blob/master/Introduction%20of%20ASTGDEMv2.pdf) for detailed user guide (recommended).

### EUDEM

EUDEMv1.1 Download Link: https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

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

3. Check the required version of GDAL Python Libraries in Terminal.
```bash
$ gdal-config --version
```

4. Download the source file (e.g., ```gdal-1.11.3.tar.gz```) of the related GDAL version (e.g., 1.11.3) from [here](http://trac.osgeo.org/gdal/wiki/DownloadSource).

5. Manually install GDAL Python Libraries in Terminal.
```bash
$ cd path/of/downloaded/gdal/package

~$ tar -xvzf gdal-{VERSION}.tar.gz
# E.g., ~$ tar -xvzf gdal-1.11.3.tar.gz

~$ cd extracted/gdal/folder
# E.g., ~$ cd gdal-1.11.3

~$ cd swig
~$ cd python
# The setup.py exists in this directory.

~$ python setup.py build_ext --include-dirs=/usr/include/gdal/
~$ python setup.py install
```

6. Try ```>>> from osgeo import gdal``` in Python. If no error occurs, the installation is completed.

## Pipeline

The pipeline of processing **ASTERGDEMv2.0** DEMs.

<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_Process_Pipeline.png" height="550">

## Usage

The directory of source DEMs is shown in the following figure.

<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/Source_DEMs_Directory.png" height="350">

1. Prepare **ASTERGDEMv2.0** source DEMs.

   1. Download DEMs ```ASTGTM2_N51W001_dem.tif``` and ```ASTGTM2_N51E000_dem.tif```.

   2. Copy DEMs to ```DATA/DATA_ASTGDEMv20/EPSG4326_s/``` folder.

2. Prepare **EUDEMv1.1** source DEM.

   1. Download DEM ```eu_dem_v11_E30N30.tif```.

   2. Copy DEM to ```DATA/DATA_EUDEMv11/``` folder and rename as ```EUDEMv11_EPSG3035.tif```.

3. To process **ASTERGDEMv2.0** DEMs, run ```run_PyDEM_London_ASTGDEMv20.py```.

4. To process **EUDEMv1.1** DEM, run ```run_PyDEM_London_EUDEMv11.py```.

## Results

- **ASTERGDEMv2.0 DEM (London) in Pseudo Mercator PCS**
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_WD.png" height="300">

- **ASTERGDEMv2.0 DEM (London) in BNG PCS**
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_UK.png" height="300">

- **ASTERGDEMv2.0 DEM (London) in LAEA PCS**
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_EU.png" height="300">

- **Elevation of 24 Locations in London (meters)**

| No.           | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 
| ------------- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- 
| ASTGDEMv20_WD | 18 | 18 | 38 | 40 | 65 | 26 | 35 | 31 | 17 | 79 | 13 | 41 | 62 | 82 | 9  | 13 | 31 | 31 | 15 | 22 | 24 | 40 | 8  | 40 
| ASTGDEMv20_UK | 14 | 14 | 36 | 25 | 60 | 37 | 33 | 40 | 20 | 68 | 12 | 25 | 62 | 59 | 15 | 18 | 22 | 22 | 15 | 21 | 14 | 33 | 8  | 47 
| ASTGDEMv20_EU | 18 | 18 | 38 | 40 | 65 | 26 | 35 | 31 | 17 | 79 | 13 | 41 | 62 | 82 | 9  | 13 | 31 | 31 | 15 | 22 | 24 | 40 | 8  | 40 
| EUDEMv11_WD   | 12 | 12 | 37 | 30 | 61 | 25 | 29 | 36 | 11 | 66 | 11 | 31 | 64 | 79 | 7  | 27 | 25 | 25 | 14 | 15 | 13 | 32 | 5  | 36 
| EUDEMv11_UK   | 12 | 12 | 37 | 26 | 58 | 30 | 32 | 35 | 11 | 71 | 8  | 30 | 66 | 78 | 8  | 26 | 24 | 24 | 8  | 16 | 13 | 32 | 9  | 35 
| EUDEMv11_EU   | 12 | 12 | 37 | 30 | 61 | 25 | 29 | 36 | 11 | 66 | 11 | 31 | 64 | 79 | 7  | 27 | 25 | 25 | 14 | 15 | 13 | 32 | 5  | 36 

<!--
- **Elevation of 5 Locations in London**
| No. | Latitude | Longitude | Elev. in WGS-84 (m)     | Elev. in OSGB-36 (m)     | Elev. in Google Earth (m) 
| --- | -------- | --------- | ----------------------- | ------------------------ | ----------------------------- 
| 1   | 51.52104 | -0.21349  | 31 (+7)                 | 22 (-1)                  | 23 
| 2   | 51.52770 | -0.12905  | 40 (+0)                 | 25 (-15)                 | 40 (Building/Road) 
| 3   | 51.42525 | -0.34560  | 24 (+12)                | 14 (+2)                  | 12 
| 4   | 51.45635 | 0.040725  | 41 (+13)                | 25 (-3)                  | 28 
| 5   | 51.45258 | 0.070766  | 79 (+14)                | 68 (+3)                  | 65 
-->

## References

[1] [EPSG 4326 vs EPSG 3857 (projections, datums, coordinate systems, and more!)](http://lyzidiamond.com/posts/4326-vs-3857)

[2] [Coordinate systems and projections for beginners](https://communityhub.esriuk.com/geoxchange/2012/3/26/coordinate-systems-and-projections-for-beginners.html)

[3] [CSDN Blog](https://blog.csdn.net/liuhailiuhai12/article/details/75007417)

<br>

<i>Please star this repository if you found its content useful. Thank you very much.</i>

<i>如果该程序对您有帮助，请为该程序加星支持哈，非常感谢。</i>

<i>Last updated: 20/03/2019</i>
