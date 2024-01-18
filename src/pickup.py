from typing import List
from model import Castle
from idokeido import calc_distance

'''
○ pickup_near5 : 開始地点から近い城を5箇所list型で返す
引数
・castles：百名城全部入ったリスト
・current_lat：開始地点の緯度
・current_lon：開始地点の経度
'''

# 開始地点から距離が近い五つの城をリストにまとめて返す関数
def pickup_near5(castles: List[Castle], current_lat: float, current_lon: float):
    distances = []
    for castle in castles:
        distance = calc_distance(current_lat, current_lon, castle.lat, castle.lng)
        distances.append((castle, distance))
    
    distances.sort(key=lambda x: x[1]) # 距離で昇順にソート

    nearest_castles = []
    for i in range(min(5, len(distances))):
        nearest_castles.append(distances[i][0])
    
    return nearest_castles



'''
○ pickup_inRadius : 開始地点から近い城を5箇所list型で返す
引数
・castles：百名城全部入ったリスト
・current_lat：開始地点の緯度
・current_lon：開始地点の経度
・radius：探索半径(km)
'''

#開始地点から探索範囲内(半径：radius)に入る城をリスト型で返す関数
def pickup_inRadius(castles, current_lat, current_lon, radius):
    # 探索範囲内の城を格納するリスト
    search_result = []

    for castle in castles:
        # 現在地と城の距離を計算
        distance = calc_distance(current_lat, current_lon, castle.lat, castle.lon)
        
        # 距離が探索範囲内の場合、リストに追加
        if distance <= radius:
            search_result.append(castle)

    return search_result
