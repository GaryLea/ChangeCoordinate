# ChangeCoordinate(坐标转换)

## 安装：
pip install ChangeCoordinate

## 使用:
``` 
from ChangeCoordinate import ChangeCoord

coord = ChangeCoord()

# 这里以百度米制坐标转wgs84坐标为例
lng = 121.xxxxxx
lat = 33.xxxxx

lng, lat = coord.bd09mc_to_wgs84(lng, lat)
```
