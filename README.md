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

### Data Characteristics


### Data Download

The ASTGDEMv2 data can be downloaded from [EarthExplorer](https://earthexplorer.usgs.gov/) (recommanded) or from [NASA Earthdata Search](https://search.earthdata.nasa.gov/search?q=ASTGTM%20V002).

#### EarthExplorer User Guide

For **EarthExplorer** users, open the webpage of [EarthExplorer](https://earthexplorer.usgs.gov/).

![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/images/01.jpg)

Click the "**Data Sets**" tag. Then, search or select the "**Digital Elevation**" category and select the "**ASTER GLOBAL DEM**" on the data list. 
![](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/images/02.jpg)


Next, set the filter criteria in the "**Additional Criteria**" tag for downloading required DEM data (see [EarthExplorer User Guide](https://lta.cr.usgs.gov/DD/ASTER_GDEM.html#entity_id_aster_gdem) or a local copy [EarthExplorer User Guide.txt](https://github.com/HeZhang1994/DEM-Digital-Elevation-Model-Tools/blob/master/EarthExplorer%20User%20Guide.txt) for more details). 

For example, to download DEM data of London (~51°N, ~0°E), set the first filter criteria as "ASTGDEMV2_0N51W001", and the second as "ASTGDEMV2_0N51E000". Then, click the "**Results**" button on the bottom of webpage. The filtered DEM data files will show on "**Results**" tag.


















