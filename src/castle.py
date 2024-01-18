#城の情報

class Castle:
    name: str   #城の名前
    lat: float    #緯度
    lon: float    #経度

    #コンストラクタ
    def __init__(self,name,lat,lon):
        self.name = name
        self.lat = lat
        self.lon = lon



