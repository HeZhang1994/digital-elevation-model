# Python Tools for Digital Elevation Model

This is the **Python** implemented tools for processing **DEM** data.

### Important Terms and Abbreviations

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

### Functions

1. **Transforming** DEM data from GCS (e.g., WGS-84) to another GCS (e.g., OSGB-36).

2. **Projecting** DEM data from GCS (e.g., WGS-84/OSGB-36) to the related PCS (e.g., Web Mercator/BNG).

3. **Re-Projecting** DEM data from PCS (e.g., ETRS-LAEA) to the related GCS (e.g., ETRS-89).

4. **Visualizing** DEM data in different PCSs as 2D images.

5. **Obtaining** elevation of specific locations from different DEM data in different GCSs.

See [RTM.txt](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/RTM.txt) for more important details.

### Limitation

1. Can not visualize 3D land surface.

### Flow Chart

* **Step 1** Pre-processing of ASTGDEMv2 data: Removing overlapped elements and merge data arrays of different tiles.

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/images/DEM_Tool_Step1.png)

* **Step 2** Processing of ASTGDEMv2 data: Transforming, projecting, visualizing DEM data and obtaining elevation values.

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/images/DEM_Tool_Step2.png)

## Environment

This code has been tested on **Ubuntu 16.04** operating system.

## Language

* __Python 3.7 (3.0+ Kernel for Jupyter Notebook)__

## Dependency

* __GDAL 1.11.3__

1. Install GDAL development libraries and export environment variables for the compiler:
```bash
$ sudo apt-get install libgdal-dev

$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal
```

2. Install GDAL Python Libraries:
```bash
$ pip install GDAL
```

If it comes with the error: ```cpl_vsi_error.h: No such file or directory```, try the following installation procedures.

3. Check the required/installed version of GDAL Python Libraries on Ubuntu operating system:
```bash
$ gdal-config --version
```

4. Download the source file (e.g., gdal-1.11.3.tar.gz) of related GDAL version (e.g., 1.11.3) from [GDAL website](http://trac.osgeo.org/gdal/wiki/DownloadSource).

5. Manually install GDAL Python Libraries:
```bash
$ cd path/of/downloaded/gdal/package

$ tar -xvzf gdal-version.tar.gz
# E.g., tar -xvzf gdal-1.11.3.tar.gz

$ cd extracted/gdal/folder
# E.g., cd gdal-1.11.3

$ cd swig
$ cd python
# The setup.py exists in this directory.

$ python setup.py build_ext --include-dirs=/usr/include/gdal/
$ python setup.py install
```

6. Try ```>>> from osgeo import gdal``` in python. If no error occurs, the installation is completed.

## Data

**ASTGDEMv2.0 data**

Download Link: https://earthexplorer.usgs.gov/

See [Introduction of ASTGDEMv2.pdf](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/Introduction%20of%20ASTGDEMv2.pdf) for details (highly recommended for tyro).

**EUDEMv1.1 data**

Download Link: https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

## Usage

To get view and get the elevation in London: 

- Download ASTGDEMv2.0 data ```ASTGTM2_N51W001_dem.tif``` and ```ASTGTM2_N51E000_dem.tif```.
- Copy ASTGDEMv2.0 data files to ```DATA/DATA_ASTGDEMv20/EPSG4326_s/``` folder.

- Download EUDEMv1.1 data ```eu_dem_v11_E30N30.tif```.
- Copy EUDEMv1.1 data file to ```DATA/DATA_EUDEMv11/EPSG3035_s/``` folder.
- Copy ```eu_dem_v11_E30N30.tif``` to ```DATA/DATA_EUDEMv11/``` folder and rename as ```EUDEMv11_EPSG3035.tif```.

Then, run Python code in ```run_ASTGDEMv2.ipynb``` (see code comments for details).

## Results

### 2D DEM image of London in Web Mercator PCS (EPSG-3857)

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/images/LD_EPSG3857.png)

### 2D DEM image of London in BNG PCS (EPSG-27700)

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/images/LD_EPSG27700.png)

### Elevation of 5 Locations in London

| No. | Latitude | Longitude | Elevation in WGS-84 (m) | Elevation in OSGB-36 (m) | Elevation in Google Earth (m) 
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

<i>Last Updated: 12/02/2019</i>
