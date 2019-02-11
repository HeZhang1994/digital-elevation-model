# Digital Elevation Model Tools

This is the **Python** implementation of **Digital Elevation Model (DEM)** tools.

### Important Terms and Abbrevations:

| Term                                   | Abbrevation | Remark 
| -------------------------------------- | :---------: | :----: 
| Digital Elevation Model                | DEM         | 
| Geographic Coordinate System           | GCS         | 3D 
| Projected Coordinate System            | PCS         | 2D 
| Georeferenced Tagged Image File Format | GeoTIFF     | 2D 



### Functions:

1. **Transforming** DEM from current GCS to another GCS.

2. **Projecting** DEM from current GCS to the corresponding PCS.

3. **Visuzlising** DEM in PCS as 2D image.

4. **Reading** elevation of specific locations from DEM in GCS.

## DEM Dataset - ASTER GDEM

The ASTER GDEM covers land surfaces between **83°N** and **83°S**. It is comrised of 22702 **1°x1° tiles**. Each tile contains at least 0.01% land surface (thats why tiles that contain only ocean area are missing XD). Its data format is **GeoTIFF (.tif)**.
