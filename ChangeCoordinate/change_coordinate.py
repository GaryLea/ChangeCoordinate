# -*- coding: utf-8 -*-
import math


class ChangeCoord(object):
    def __init__(self):
        """
        初始化参数
        :param mcband, mc211 : 百度平面转经纬参数
        :param x_pi : x pi值
        :param pi : PI值
        :param a : 长半轴
        :param ee : 偏心率平方
        """
        self.mcband = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
        self.mc2ll = [
            [1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547,
             91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2],
            [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846, -1.85204757529826,
             -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86],
            [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871,
             -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
            [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277,
             -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
            [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511,
             -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
            [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994,
             -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5], ]

        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = 3.1415926535897932384626  # π
        self.a = 6378245.0  # 长半轴
        self.ee = 0.00669342162296594323  # 偏心率平方

    def convert(self, lng, lat, f):
        """
        平面转经纬计算公式
        :param lng:  经度
        :param lat: 纬度
        :param f: 百度平面转经纬参数其中一行
        """
        if len(f) == 0:
            return 0, 0

        tlng = f[0] + f[1] * math.fabs(lng)
        cc = math.fabs(lat) / f[9]
        tlat = 0.0
        for index in range(7):
            tlat += (f[index + 2] * math.pow(cc, index))

        if lng < 0:
            tlng *= -1

        if lat < 0:
            tlat *= -1

        return tlng, tlat

    def db09mc_to_bd09(self, mercartorX, mercartorY):
        """
        百度平面转经纬
        :param mercartorX : 百度平面经度
        :param mercartorY : 百度平面纬度
        :return 转换后的百度经纬坐标
        """
        mercartorX, mercartorY = math.fabs(mercartorX), math.fabs(mercartorY)
        f = []
        index = 0
        for mcb in self.mcband:
            if mercartorY >= mcb:
                f = self.mc2ll[index]
                break
            index += 1
        if f == []:
            index = 0
            for mcb in self.mcband:
                if -mercartorY <= mcb:
                    f = self.mc2ll[index]
                    break
                index += 1

        return self.convert(mercartorX, mercartorY, f)

    def gcj02_to_bd09(self, lng, lat):
        """
        火星坐标系(GCJ-02)转百度坐标系(BD-09)
        谷歌、高德——>百度
        :param lng:火星坐标经度
        :param lat:火星坐标纬度
        :return:
        """
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * self.x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lng, bd_lat]

    def bd09_to_gcj02(self, lng, lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x = lng - 0.0065
        y = lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return [gg_lng, gg_lat]

    def wgs84_to_gcj02(self, lng, lat):
        """
        WGS84转GCJ02(火星坐标系)
        :param lng:WGS84坐标系的经度
        :param lat:WGS84坐标系的纬度
        :return:
        """
        if self.out_of_china(lng, lat):  # 判断是否在国内
            return [lng, lat]
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [mglng, mglat]

    def gcj02_to_wgs84(self, lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:
        """
        if self.out_of_china(lng, lat):
            return [lng, lat]
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    def bd09_to_wgs84(self, lng, lat):
        """
        bd09 转 wgs84坐标
        :param lng: 百度经度
        :param lat: 百度纬度
        :return:
        """
        lng, lat = self.bd09_to_gcj02(lng, lat)
        return self.gcj02_to_wgs84(lng, lat)

    def wgs84_to_bd09(self, lng, lat):
        """
        wgs84坐标转bd09
        :param lng: wgs84经度
        :param lat: wgs84纬度
        :return: bd_09坐标
        """
        location_gjf02 = self.wgs84_to_gcj02(lng, lat)
        bd09_localhost = self.gcj02_to_bd09(location_gjf02[0],location_gjf02[1])
        return bd09_localhost

    def bd09mc_to_wgs84(self, lng, lat):
        """
        百度平面转wgs84坐标
        :param lng : 经度
        :param lat : 纬度
        :return 转换后的wgs84经纬坐标
        """
        location_bd09 = self.db09mc_to_bd09(lng, lat)
        location_gcj02 = self.bd09_to_gcj02(location_bd09[0], location_bd09[1])
        location_wgs84 = self.gcj02_to_wgs84(location_gcj02[0], location_gcj02[1])
        return location_wgs84

    def _transformlat(self, lng, lat):
        """计算"""
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng:
        :param lat:
        :return:
        """
        return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


if __name__ == '__main__':
    lon = 11915544.30
    lat = 3881104.12
    change_map = ChangeCoord()
    # result = change_map.db09mc_to_bd09(lon, lat)
    # result2 = change_map.bd09_to_gcj02(result[0], result[1])
    # result3 = change_map.gcj02_to_wgs84(result2[0], result2[1])
    # print(result)
    # print(result2)
    # print(result3)
    lng, lat = change_map.bd09mc_to_wgs84(lon,lat)
    print(lng)

