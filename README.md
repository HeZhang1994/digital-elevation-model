# Digital Elevation Model Python Tools

This is the **Python** implemented tools of processing **Digital Elevation Model (DEM)**.

### Important Terms and Abbrevations

| Term                                   | Abbrevation | Remark 
| -------------------------------------- | ----------- | ------ 
| Digital Elevation Model                | DEM         | 
| Geographic Coordinate System           | GCS         | [Longitude, Latitude, Elevation] on 3D spheriod 
| Projected Coordinate System            | PCS         | [X-axis, Y-axis, Elevation] on 2D plane 
| Georeferenced Tagged Image File Format | GeoTIFF     | DEM image/data format (.tif) 
| 1984 World Geodetic System             | WGS-84      | GCS, approximating the spheriod of Earth 
| Web Mercator or Pseudo Mercator        | -           | PCS of WGS-84 
| 1936 Ordnance Survey Great Britain     | OSGB-36     | GCS, approximating the spheriod of Britain 
| British National Grid                  | BNG         | PCS of OSGB-36 
| European Petroleum Survey Group        | EPSG        | EPSG codes define different GCSs and PCSs 

### Functions

1. **Transforming** DEM from current GCS (e.g., WGS-84) to another GCS (e.g., OSGB-36).

2. **Projecting** DEM from current GCS (e.g., WGS-84/OSGB-36) to the corresponding PCS (e.g., Web Mercator/BNG).

3. **Visualising** DEM in PCS as 2D image.

4. **Reading** elevation of specific location from DEM in GCS.

### Limitation

1. Can not visualize 3D land surface.

### Flow Chart

fig tbc...

## Environment

This code has been tested on **Ubuntu 16.04** operating system.

## Language

* __Python 3.7 (3.0+ Kernel for Jupyter Notebook)__

## Dependency

* __GDAL 1.11.3__

To begin with, install GDAL development libraries and export environment variables for the compiler:
```bash
$ sudo apt-get install libgdal-dev

$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal
```

Then, install GDAL Python Libraries:
```bash
$ pip install GDAL
```

If it comes with the error: ```cpl_vsi_error.h: No such file or directory```, try the following installation procedures.

Check the required/installed version of GDAL Python Libraries on your Ubuntu operating system:
```bash
$ gdal-config --version
```

Download the source file (e.g., gdal-1.11.3.tar.gz) of related GDAL version (e.g., 1.11.3) from [GDAL website](http://trac.osgeo.org/gdal/wiki/DownloadSource).

Manually install GDAL Python Libraries:
```bash
$ cd path/of/downloaded/gdal/package

$ tar -xvzf gdal-version.tar.gz 
# E.g., tar -xvzf gdal-1.11.3.tar.gz

$ cd extracted/gdal/folder
# E.g., cd gdal-1.11.3

$ cd swig
$ cd python
# setup.py exists under this directory.

$ python setup.py build_ext --include-dirs=/usr/include/gdal/
$ python setup.py install
```

Try ```from osgeo import gdal``` in python. If it does not come with any error, the installation is completed.

## DEM Data

ASTER GDEM data are used in this code. See [Intorduction of ASTER GDEM data.pdf](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/Intorduction%20of%20ASTER%20GDEM%20data.pdf) for more details.

## Usage

Download and copy ASTGDEMv2 data of London (```ASTGTM2_N51W001_dem.tif``` and ```ASTGTM2_N51E000_dem.tif```) to ```DATA_ASTGDEMv2/EPSG4326/``` folder.

Then, run Python code in ```run_ASTGDEMv2.ipynb``` (see comments for more details).

## Results

2D DEM image of London in Web Meractor PCS (EPSG-3857):

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/LD_EPSG3857.png)

2D DEM image of London in BNG PCS (EPSG-27700):

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/LD_EPSG27700.png)

## References (Highly Recommended for Tyro)

[1] [EPSG 4326 vs EPSG 3857 (projections, datums, coordinate systems, and more!)](http://lyzidiamond.com/posts/4326-vs-3857)

[2] [Coordinate systems and projections for beginners](https://communityhub.esriuk.com/geoxchange/2012/3/26/coordinate-systems-and-projections-for-beginners.html)

[3] [CSDN Blog](https://blog.csdn.net/liuhailiuhai12/article/details/75007417)
