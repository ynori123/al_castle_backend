from castle import Castle
from pickup import pickup_inRadius
from pickup import pickup_near5
from idokeido import calc_distance

# テストメソッド
def test_pickup_near5():
    # 城のリストを作成
    castles = [
        Castle("Castle A", 35.6895, 139.6917),
        Castle("Castle B", 34.6863, 135.5197),
        Castle("Castle C", 35.6892, 139.6921),
        Castle("Castle D", 35.6890, 139.6923),
        Castle("Castle E", 35.6888, 139.6925),
        Castle("Castle F", 35.6886, 139.6927),
        Castle("Castle G", 35.6884, 139.6929),
        Castle("Castle H", 35.6882, 139.6931),
        Castle("Castle I", 35.6880, 139.6933),
        Castle("Castle J", 35.6878, 139.6935)
    ]

    # 現在地の緯度・経度を指定
    current_lat = 35.6891
    current_lon = 139.6917

    # 距離が短い五つの城を取得
    nearest_castles = pickup_near5(castles, current_lat, current_lon)

    # 結果を表示
    for castle in nearest_castles:
        print(castle.name)


def test_pickup_inRadius():
    # テスト用の城データ
    castles = [
        Castle("城1", 35.123, 139.456),
        Castle("城2", 35.678, 139.789),
        Castle("城3", 36.123, 140.456),
        Castle("城4", 34.123, 139.456),
        Castle("城5", 35.0, 140.0)
    ]

    # 現在地の緯度・経度と探索範囲の半径
    current_lat = 35.0
    current_lon = 139.0
    radius = 100.0

    # 検索結果の期待値
    expected_result = [
        Castle("城1", 35.123, 139.456),
        Castle("城5", 35.0, 140.0)
    ]

    # 探索結果を取得
    result = pickup_inRadius(castles, current_lat, current_lon, radius)

    # 検証
    assert len(result) == len(expected_result)
    for i in range(len(result)):
        assert result[i].name == expected_result[i].name
        assert result[i].lat == expected_result[i].lat
        assert result[i].lon == expected_result[i].lon
        

def test_calc_distance() -> None:
    # テスト用の緯度・経度
    lat1 = 35.6895
    lon1 = 139.6917
    lat2 = 34.7025
    lon2 = 135.4958

    # 二地点間の距離を計算
    distance = calc_distance(lat1, lon1, lat2, lon2)
    print("地点A ",lat1,",",lon1,"\n地点B ",lat2,",",lon2,"\n距離:",distance,"\n")
    
    #検証
    assert abs(distance - 397.461944) <= 1