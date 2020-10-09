# 基于Python的数字高程模型处理

[![image](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HeZhang1994/digital-elevation-model/blob/master/LICENSE)
[![image](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()
[![image](https://img.shields.io/badge/python-3.7-blue.svg)]()
[![image](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

[*English Version*](https://github.com/HeZhang1994/digital-elevation-model/blob/master/README.md) | [*中文版*](https://github.com/HeZhang1994/digital-elevation-model/blob/master/README-cn.md)

基于**Python**实现的变换、投影、转换和可视化**数字高程模型**并且读取其中给定位置的海拔值。

## 目录

- [专业术语和缩略词](#专业术语和缩略词)
- [功能](#功能)
- [数字高程模型数据](#数字高程模型数据)
  - [ASTERGDEM](#astergdem)
  - [EUDEM](#eudem)
- [依赖项](#依赖项)
- [ASTERGDEM处理流程图](#astergdem处理流程图)
- [使用方法](#使用方法)
  - [ASTERGDEM的使用方法](#astergdem的使用方法)
  - [EUDEM的使用方法](#eudem的使用方法)
- [结果](#结果)
  - [伦敦数字高程模型图像](#伦敦数字高程模型图像)
  - [伦敦海拔](#伦敦海拔)
- [参考](#参考)

## 专业术语和缩略词

| 专业术语                                     | 缩略词        | 备注
| ------------------------------------------ | ------------ | ------
| Digital Elevation Model 数字高程模型         | DEM          | -
| Geographic Coordinate System 地理坐标系      | GCS          | 三维椭球面，[经度，纬度，海拔]
| Projected Coordinate System 投影坐标系       | PCS          | 二维平面，[横坐标，纵坐标，海拔]
| Georeferenced Tagged Image File Format     | GeoTIFF      | 数字高程模型的文件格式
| European Petroleum Survey Group            | EPSG         | EPSG代码用于识别不同GCS和PCS
| 1984 World Geodetic System                 | WGS-84       | **GCS**, *EPSG-4326*, 参考椭球面位于地球
| Pseudo Mercator (Web Mercator)             | -            | **PCS** of WGS-84, *EPSG-3857*
| 1936 Ordnance Survey Great Britain         | OSGB-36      | **GCS**, *EPSG-4277*, 参考椭球面位于英国
| British National Grid                      | BNG          | **PCS** of OSGB-36, *EPSG-27700*
| 1989 European Terrestrial Reference System | ETRS-89      | **GCS**, *EPSG-4258*, 参考椭球面位于地球
| Lambert Azimuthal Equal-Area               | LAEA         | **PCS** of ETRS-89, *EPSG-3035*

## 功能

- **变换**地理坐标系下DEM至其他地理坐标系（例如，由WGS-84变换至OSGB-36）。

- **投影**地理坐标系下的DEM至对应的投影坐标系（例如，由OSGB-36投影至BNG）。

- **转换**投影坐标系下的DEM至对应的地理坐标系（例如，由LAEA转换至ETRS-89）。

- **可视化**投影坐标系下的DEM为二维图像。

- **读取**地理坐标系下的DEM中给定位置的海拔值。

## 数字高程模型数据

### ASTERGDEM

- **更新** ASTER数据集的获取和下载，参见[链接](https://asterweb.jpl.nasa.gov/gdem.asp)。

- ~~ASTERGDEMv2.0下载链接：https://earthexplorer.usgs.gov/~~

- ~~关于详细介绍和使用指南，参见[Introduction of ASTGDEMv2.pdf](https://github.com/HeZhang1994/digital-elevation-model/blob/master/Introduction%20of%20ASTGDEMv20.pdf)。~~

### EUDEM

- EUDEMv1.1下载链接：https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1

- 关于详细介绍和使用指南，参见[这里](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1?tab=metadata)。

## 依赖项

* __gdal (osgeo) 1.11.3__
* __matplotlib 3.0.2__
* __numpy 1.15.4__
* __pandas 0.23.4__

下述**GDAL**安装步骤（1-2）总结自[mothergeo](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html)。

1. 在终端安装**GDAL Development Libraries**并将环境变量导出至编译器。
```bash
$ sudo apt-get install libgdal-dev

$ export CPLUS_INCLUDE_PATH=/usr/include/gdal
$ export C_INCLUDE_PATH=/usr/include/gdal
```

2. 在终端安装**GDAL Python Libraries**。
```bash
$ pip install GDAL
```

如果出现*错误*：`cpl_vsi_error.h: No such file or directory`，请尝试下述步骤。

3. 在终端查看**GDAL Python Libraries**所需的版本。
```bash
$ gdal-config --version
```

4. 下载对应GDAL版本（例如，`1.11.3`）的源文件（例如，`gdal-1.11.3.tar.gz`）自[这里](http://trac.osgeo.org/gdal/wiki/DownloadSource)。

5. 在终端手动安装**GDAL Python Libraries**。
```bash
$ cd path/of/downloaded/gdal/package

~$ tar -xvzf gdal-{VERSION}.tar.gz
# 例如， ~$ tar -xvzf gdal-1.11.3.tar.gz

~$ cd extracted/gdal/folder
# 例如， ~$ cd gdal-1.11.3

~$ cd swig
~$ cd python
# setup.py存在于该目录下。

~$ python setup.py build_ext --include-dirs=/usr/include/gdal/
~$ python setup.py install
```

6. 在Python中运行`>>> from osgeo import gdal`。如果没有报错，则安装完成。

## ASTERGDEM处理流程图

<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_Process_Pipeline.png" height="550">

## 使用方法

原始DEM文件的目录列表如下。
<pre><code>
└── Data/
    ├── DATA_ASTGDEMv20/
    │   └── EPSG4326_s/
    │       ├── ASTGTM2_N51W001_dem.tif
    │       └── ASTGTM2_N51E000_dem.tif
    └── DATA_EUDEMv11/
        └── EUDEMv11_EPSG3035.tif
</code></pre>

### ASTERGDEM的使用方法

1. 下载DEM文件`ASTGTM2_N51W001_dem.tif`和`ASTGTM2_N51E000_dem.tif`自[这里](https://earthexplorer.usgs.gov/)。

2. 复制DEM文件到文件夹`DATA/DATA_ASTGDEMv20/EPSG4326_s/`。

3. 运行`run_DEM_ASTGDEMv20.py`或`run_DEM_ASTGDEMv20_ipy.ipynb`，以处理ASTERGDEMv2.0的数字高程模型。

4. 运行`run_DEM_ASTGDEMv20.py`的日志可以参见`Log_run_DEM_ASTGDEMv20.txt`。

### EUDEM的使用方法

1. 下载DEM文件`eu_dem_v11_E30N30.tif`自[这里](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1)。

2. 复制DEM文件到文件夹`DATA/DATA_EUDEMv11/`并重命名为`EUDEMv11_EPSG3035.tif`。

3. 运行`run_DEM_EUDEMv11.py`或`run_DEM_EUDEMv11_ipy.ipynb`，以处理EUDEMv1.1的数字高程模型。

4. 运行`run_DEM_EUDEMv11.py`的日志可以参见`Log_run_DEM_EUDEMv11.txt`。

## 结果

### 伦敦数字高程模型图像

- **Pseudo Mercator**投影坐标系下的ASTERGDEMv2.0图像 
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_WD.png" height="300">

- **BNG**投影坐标系下的ASTERGDEMv2.0图像 
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_UK.png" height="300">

- **LAEA**投影坐标系下的ASTERGDEMv2.0图像 
<img src="https://github.com/HeZhang1994/digital-elevation-model/blob/master/images/ASTGDEMv20_EU.png" height="300">

### 伦敦海拔

- 伦敦24个位置的海拔值（米）

| No. of Location | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24
| --------------- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | --
| ASTGDEMv20_WD   | 18 | 18 | 38 | 40 | 65 | 26 | 35 | 31 | 17 | 79 | 13 | 41 | 62 | 82 | 9  | 13 | 31 | 31 | 15 | 22 | 24 | 40 | 8  | 40
| ASTGDEMv20_UK   | 14 | 14 | 36 | 25 | 60 | 37 | 33 | 40 | 20 | 68 | 12 | 25 | 62 | 59 | 15 | 18 | 22 | 22 | 15 | 21 | 14 | 33 | 8  | 47
| ASTGDEMv20_EU   | 18 | 18 | 38 | 40 | 65 | 26 | 35 | 31 | 17 | 79 | 13 | 41 | 62 | 82 | 9  | 13 | 31 | 31 | 15 | 22 | 24 | 40 | 8  | 40
| EUDEMv11_WD     | 12 | 12 | 37 | 30 | 61 | 25 | 29 | 36 | 11 | 66 | 11 | 31 | 64 | 79 | 7  | 27 | 25 | 25 | 14 | 15 | 13 | 32 | 5  | 36
| EUDEMv11_UK     | 12 | 12 | 37 | 26 | 58 | 30 | 32 | 35 | 11 | 71 | 8  | 30 | 66 | 78 | 8  | 26 | 24 | 24 | 8  | 16 | 13 | 32 | 9  | 35
| EUDEMv11_EU     | 12 | 12 | 37 | 30 | 61 | 25 | 29 | 36 | 11 | 66 | 11 | 31 | 64 | 79 | 7  | 27 | 25 | 25 | 14 | 15 | 13 | 32 | 5  | 36

## 参考

[1] [EPSG 4326 vs EPSG 3857 (projections, datums, coordinate systems, and more!)](http://lyzidiamond.com/posts/4326-vs-3857)

[2] [Coordinate systems and projections for beginners](https://communityhub.esriuk.com/geoxchange/2012/3/26/coordinate-systems-and-projections-for-beginners.html)

[3] [CSDN博客](https://blog.csdn.net/liuhailiuhai12/article/details/75007417)

<br>

<i>如果您对该项目有任何问题，请报告issue，我将会尽快回复。</i>

<i>如果该项目对您有帮助，请为其加星支持哈，非常感谢。^_^</i>
