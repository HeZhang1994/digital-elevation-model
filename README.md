# Digital Elevation Model Python Tools

This is the **Python** implemented tools of processing **Digital Elevation Model (DEM)**.

### Important Terms and Abbrevations

| Term                                   | Abbrevation | Remark 
| -------------------------------------- | :---------: | :----: 
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

### Flow Chart

fig

### Limitation

1. Can not visualize 3D land surface.

## Environment

This code has been tested on **Ubuntu 16.04** operating system.

## Language

* __Python 3.7 (3.0+)__

## Dependency

* __GDAL 1.11.3__

To begin with, install GDAL development libraries and export environment variables for the compiler:
```bash
$ sudo apt-get install libgdal-dev

$ export environment variables for the compiler
$ export C_INCLUDE_PATH=/usr/include/gdal
```

Then, install GDAL Python Libraries:
```bash
$ pip install GDAL
# or
$ pip3 install GDAL
# if both py2 and py3 exist on your operating system.
```

If it comes with the error: cpl_vsi_error.h: No such file or directory, try the following installation procedures.

Check the required/installed version of GDAL Python Libraries on your Ubuntu operating system:
```bash
$ gdal-config --version
```

Download the source file (e.g., gdal-1.11.3.tar.gz) of related GDAL version (e.g., 1.11.3) from [GDAL website](http://trac.osgeo.org/gdal/wiki/DownloadSource).

## DEM Data

ASTER GDEM data are used in this code. See [Intorduction of ASTER GDEM data.pdf](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/Intorduction%20of%20ASTER%20GDEM%20data.pdf) for more details.

## Results

res





