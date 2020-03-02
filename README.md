# Python for Processing Digital Elevation Models

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/digital-elevation-model/blob/master/LICENSE)
[![image](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/digital-elevation-model/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/digital-elevation-model/blob/master/README-cn.md)

This is a **Python** implementation of transforming, projecting, converting and visualizing **Digital Elevation Models** as well as reading their elevation of given locations.

## Table of Contents

- [Terms and Abbreviations](#terms-and-abbreviations)
- [Functions](#functions)
- [DEM Data](#dem-data)
  - [ASTERGDEM](#astergdem)
  - [EUDEM](#eudem)
- [Dependencies](#dependencies)
- [Pipeline of Processing ASTERGDEM](#pipeline-of-processing-astergdem)
- [Usage](#usage)
  - [Usage of ASTERGDEM](#usage-of-astergdem)
  - [Usage of EUDEM](#usage-of-eudem)
- [Results](#results)
  - [DEM Images of London](#dem-images-of-london)
  - [Elevation of London](#elevation-of-london)
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

- **Projecting** DEM from one GCS (e.g., OSGB-36) to the related PCS (e.g., BNG).

- **Converting** DEM from one PCS (e.g., LAEA) to the related GCS (e.g., ETRS-89).

- **Visualizing** DEM in PCS as a 2D image.

- **Reading** the elevation of given locations from DEM in GCS.

## DEM Data

### ASTERGDEM

- ASTERGDEMv2.0 download link: https://earthexplorer.usgs.gov/

- See [Introduction of ASTGDEMv20.pdf](https://github.com/HeZhang1994/digital-elevation-model/blob/master/Introduction%20of%20ASTGDEMv20.pdf) for detailed introduction and user guide (recommended).

### EUDEM

- EUDEMv1.1 download link: https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

- See [here](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1?tab=metadata) for detailed introduction and user guide.

## Dependencies

* __gdal (osgeo) 1.11.3__
* __matplotlib 3.0.2__
* __numpy 1.15.4__
* __pandas 0.23.4__

The following procedures (1-2) for installing **GDAL** are recapitulated from [mothergeo](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html).

1. Install **GDAL Development Libraries** and export environment variables for the compiler in Terminal.
```bash
$ sudo apt-get install libgdal-dev

$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal
```

2. Install **GDAL Python Libraries** in Terminal.
```bash
$ pip install GDAL
```

If it comes with the *error*: `cpl_vsi_error.h: No such file or directory`, please try the following procedures.

3. Check the required version of **GDAL Python Libraries** in Terminal.
```bash
$ gdal-config --version
```

4. Download the source file (e.g., `gdal-1.11.3.tar.gz`) of the related GDAL version (e.g., `1.11.3`) from [here](http://trac.osgeo.org/gdal/wiki/DownloadSource).

5. Manually install **GDAL Python Libraries** in Terminal.
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

6. Run `>>> from osgeo import gdal` in Python. If no error occurs, the installation is accomplished.

## Pipeline of Processing ASTERGDEM

<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_Process_Pipeline.png" height="550">

## Usage

The directory of source DEMs is shown as below.
<pre><code>
└── Data/
    ├── DATA_ASTGDEMv20/
    │   └── EPSG4326_s/
    │       ├── ASTGTM2_N51W001_dem.tif
    │       └── ASTGTM2_N51E000_dem.tif
    └── DATA_EUDEMv11/
        └── EUDEMv11_EPSG3035.tif
</code></pre>

### Usage of ASTERGDEM

1. Download DEMs `ASTGTM2_N51W001_dem.tif` and `ASTGTM2_N51E000_dem.tif` from [here](https://earthexplorer.usgs.gov/).

2. Copy DEMs to the folder `DATA/DATA_ASTGDEMv20/EPSG4326_s/`.

3. To process ASTREGDEMv2.0 DEMs, run `run_DEM_ASTGDEMv20.py` or `run_DEM_ASTGDEMv20_ipy.ipynb`.

4. The log of running `run_DEM_ASTGDEMv20.py` can be seen in `Log_run_DEM_ASTGDEMv20.txt`.

### Usage of EUDEM

1. Download DEM `eu_dem_v11_E30N30.tif` from [here](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1).

2. Copy DEM to the folder `DATA/DATA_EUDEMv11/` and rename it as `EUDEMv11_EPSG3035.tif`.

3. To process EUDEMv1.1 DEM, run `run_DEM_EUDEMv11.py` or `run_DEM_EUDEMv11_ipy.ipynb`.

4. The log of running `run_DEM_EUDEMv11.py` can be seen in `Log_run_DEM_EUDEMv11.txt`.

## Results

### DEM Images of London

- The DEM Image of ASTERGDEMv2.0 in **Pseudo Mercator** PCS
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_WD.png" height="300">

- The DEM Image of ASTERGDEMv2.0 in **BNG** PCS
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_UK.png" height="300">

- The DEM Image of ASTERGDEMv2.0 in **LAEA** PCS
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_EU.png" height="300">

### Elevation of London

- The elevation of 24 locations in London (meter)

| No. of Location | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24
| --------------- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | --
| ASTGDEMv20_WD   | 18 | 18 | 38 | 40 | 65 | 26 | 35 | 31 | 17 | 79 | 13 | 41 | 62 | 82 | 9  | 13 | 31 | 31 | 15 | 22 | 24 | 40 | 8  | 40
| ASTGDEMv20_UK   | 14 | 14 | 36 | 25 | 60 | 37 | 33 | 40 | 20 | 68 | 12 | 25 | 62 | 59 | 15 | 18 | 22 | 22 | 15 | 21 | 14 | 33 | 8  | 47
| ASTGDEMv20_EU   | 18 | 18 | 38 | 40 | 65 | 26 | 35 | 31 | 17 | 79 | 13 | 41 | 62 | 82 | 9  | 13 | 31 | 31 | 15 | 22 | 24 | 40 | 8  | 40
| EUDEMv11_WD     | 12 | 12 | 37 | 30 | 61 | 25 | 29 | 36 | 11 | 66 | 11 | 31 | 64 | 79 | 7  | 27 | 25 | 25 | 14 | 15 | 13 | 32 | 5  | 36
| EUDEMv11_UK     | 12 | 12 | 37 | 26 | 58 | 30 | 32 | 35 | 11 | 71 | 8  | 30 | 66 | 78 | 8  | 26 | 24 | 24 | 8  | 16 | 13 | 32 | 9  | 35
| EUDEMv11_EU     | 12 | 12 | 37 | 30 | 61 | 25 | 29 | 36 | 11 | 66 | 11 | 31 | 64 | 79 | 7  | 27 | 25 | 25 | 14 | 15 | 13 | 32 | 5  | 36

## References

[1] [EPSG 4326 vs EPSG 3857 (projections, datums, coordinate systems, and more!)](http://lyzidiamond.com/posts/4326-vs-3857)

[2] [Coordinate systems and projections for beginners](https://communityhub.esriuk.com/geoxchange/2012/3/26/coordinate-systems-and-projections-for-beginners.html)

[3] [CSDN Blog](https://blog.csdn.net/liuhailiuhai12/article/details/75007417)

<br>

<i>Please report an issue if you have any question about this repository, I will respond ASAP.</i>

<i>Please star this repository if you found its content useful. Thank you very much. ^_^</i>
