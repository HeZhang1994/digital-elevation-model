# Digital Elevation Model Tools

This is the **Python** implemented tools of processing **Digital Elevation Model (DEM)**.

### Important Terms and Abbrevations:

| Term                                   | Abbrevation | Remark 
| -------------------------------------- | :---------: | :----: 
| Digital Elevation Model                | DEM         | 
| Geographic Coordinate System           | GCS         | [Longitude, Latitude, Elevation] on 3D spheriod 
| Projected Coordinate System            | PCS         | [X-axis, Y-axis, Elevation] on 2D plane 
| Georeferenced Tagged Image File Format | GeoTIFF     | DEM data format (.tif) 
| World Geodetic System 1984             | WGS-84      | GCS, approximating the spheriod of earth 
| Web Mercator or Pseudo Mercator        | -           | PCS of WGS-84 
| Ordnance Survey Great Britain 1936     | OSGB-36     | GCS, approximating the spheriod of Britain   
| British National Grid                  | BNG         | PCS of OSGB-36 
| European Petroleum Survey Group        | EPSG        | EPSG codes define different GCSs and PCSs 

### Functions:

1. **Transforming** DEM from current GCS (e.g., WGS-84) to another GCS (e.g., OSGB-36).

2. **Projecting** DEM from current GCS (e.g., WGS-84/OSGB-36) to the corresponding PCS (e.g., Web Mercator/BNG).

3. **Visualising** DEM in PCS as 2D image.

4. **Reading** elevation of specific location from DEM in GCS.

### Limitations:

1. Can not visualize 3D land surface.


## DEM Dataset - ASTER GDEM

The Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER) Global Digital Elevation Model (GDEM), i.e., ASTER GDEM or ASTGDEM, is a product of the Ministry of Economy, Trade, and Industry (METI) in Japan and the National Aeronautic and Space Administration (NASA) in United States. The source data were collected by the **Advanced Spaceborne Thermal Emission and Reflection Radiometer** on the NASA spacecraft **Terra**. The ASTGDEM version 1 (ASTGDEMv1) dara were released on 2009 and the ASTGDEM version 2 (ASTGDEMv2) data were released on 2011. The ASTGDEMv2 data are used in this code (reasons are explained below).

### Data Characteristics

The ASTGDEMv2 covers land surfaces between **83°N** and **83°S**. It is comrised of 22702 **1°x1° tiles**. Each tile is a block of earch surface that contains at least 0.01% land area. Thus, do not be surprised that tiles which contain only ocean area are missing. The ASTGDEMv2 is distributed in **GeoTIFF (.tif)** data format. The data are posted on a **1 arc-second (~30m at the equator)** grid and referenced in **WGS-84 GCS**. In this case, <span style="border-bottom:2px dashed black;">the column of data array represents the longitude, and the row represents the latitude of a specific location</span>. 

### Download

ASTGDEMv2 data can be downloaded from [EarthExplorer](https://earthexplorer.usgs.gov/) (recommanded) or from [NASA Earthdata Search](https://search.earthdata.nasa.gov/search?q=ASTGTM%20V002).

For EarthExplorer users, 





















