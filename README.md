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

### Limitation

1. Can not visualize 3D land surface.


## DEM Data - ASTGDEMv2

The Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER) Global Digital Elevation Model (GDEM), i.e., ASTER GDEM or ASTGDEM, is a product of the Ministry of Economy, Trade, and Industry (METI) in Japan and the National Aeronautic and Space Administration (NASA) in United States. The source data were collected by the **Advanced Spaceborne Thermal Emission and Reflection Radiometer** on the NASA spacecraft **Terra**. The ASTGDEM version 1 (ASTGDEMv1) dara were released on 2009 and the ASTGDEM version 2 (ASTGDEMv2) data were released on 2011. The ASTGDEMv2 data are used in this code (reasons are explained below).

### Data Characteristics

- The ASTGDEMv2 is comrised of 22702 tiles covering land surfaces between **83°N** and **83°S**. Each tile is a **1°x1°** block of earch surface that contains at least 0.01% land area. Thus, tiles which contain only ocean area are missing.

&#8195; &#8194; **Remark**: The advantage of using 1°x1° tiles is that its much more efficient for geographic data processing in a small region. For example, covering the main area of London requires only two tiles.

- The ASTGDEMv2 is distributed in **GeoTIFF (.tif)** image/data format. The data are posted on a **1 arc-second (1"~30m at the equator)** grid. The size of each tile is 1°x1° or **3601"x3601"**.

&#8195; &#8194; **Remark**: The four edges of each tile are overlapped with its four adjacent tiles. Users should remove overlapped elements and merge the related tiles when more than one tile is used.

- The ASTGDEMv2 data are referenced in **WGS-84 GCS**. In this case, the [**column**, **row**] of image/data array of one tile represents the [**longitude**, **latitude**] of a specific location on the Earth.

&#8195; &#8194; **Remark**: The WGS-84 useing a reference ellipsoid to approxiate the overall surface of the Earth. Thus, it might be not accurate in local regions. This is why we transform WGS-84 GCS to OSGB-36 GCS, which uses another reference ellipsoid to accurately describing locations in Britain.

- The ASTGDEMv2 data package (.zip) is named as, e.g., ASTGTM2_N51W001.zip, where "N51" and "W001" denote the approxied latitude and longitude of the geospatial location of bottom-left (southwest) corner. Each package includes three files: A readme file (.pdf), a dem file (\_dem.tif), and a quality assessment file (\_num.tif). The dem file (\_dem.tif) contains elevation data.

&#8195; &#8194; **Remark**: The file name only provide **approximeated** latitude and logitude of bottom-left corner. Users are required to use the latitude and longitude recorded in GeoTransform parameters of dem file.

**Summary**: The ASTGDEMv2 has **high resolution (~30m)**, **high accuracy (<20m)**, and **great land coverage (~80% of the Earth)**. Thus, the ASTGDEMv2 data are used in this code.

### Data Download

The ASTGDEMv2 data can be downloaded from [EarthExplorer](https://earthexplorer.usgs.gov/) (recommanded) or from [NASA Earthdata Search](https://search.earthdata.nasa.gov/search?q=ASTGTM%20V002).

#### EarthExplorer User Guide

For **EarthExplorer** users, open the webpage of [EarthExplorer](https://earthexplorer.usgs.gov/). Click the "**Data Sets**" tag. Then, search or select the "**Digital Elevation**" category and select the "**ASTER GLOBAL DEM**" on the data list. Next, set the filter criteria in the "**Additional Criteria**" tag for downloading required DEM data (click ["**Entity ID**"](https://lta.cr.usgs.gov/DD/ASTER_GDEM.html#entity_id_aster_gdem) under "**Additional Criteria**" tag or see [EarthExplorer User Guide.txt](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/EarthExplorer%20User%20Guide.txt) for more details). 

For example, to download DEM data of London (51°N, 0°E), set the  


















