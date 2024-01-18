# API Document
## ER Diagram
```mermaid
erDiagram
castles ||--|{ restaurants : ""
"users(余裕があれば)" ||--o{ "fell_castles(余裕があれば)" : ""
"fell_castles(余裕があれば)" ||--|| castles : ""
castles }|--|| castle_distances : ""

"users(余裕があれば)"{
    bigint id PK
    varchar name 
    barchar password 
}
"fell_castles(余裕があれば)"{
    bigint id PK
    bigint user_id FK
    bigint castle_id FK
    timestamp created_at
}
castles {
    bigint id PK
    varchar name
    varchar prefecture "都道府県"
    float lat "緯度(北緯)"
    float lng "経度(東経)"
    varchar holiday "定休日"
    varchar admission_time "入場可能時間"
    bigint admission_fee "入場料"
    varchar stamp "スタンプ設置場所"    
}
restaurants { 
    bigint id PK
    bigint castle_id FK 
    varchar name
    varchar time "営業時間"
    varchar holiday "定休日"
    varchar genre "ジャンル"
    varchar url 
}
castle_distances {
    bigint id PK
    bigint castle_id1 FK
    bigint castle_id2 FK
    double direct_distance "直線距離"
    double way_distance "道のりの距離"
    datetime time "GoogleMap APIから取得したもの"
}
```
## Endpoints
|Request Method|Route|Summary|
|---|---|---|
|GET|/ping|通信確認|
|GET|/castles|城の情報|
|GET|/castles/{castle_id}|城の詳細情報|
|POST|/travel|最短経路検索|
|POST|/user/signin|(時間があれば)ログイン|
|POST|/user/signup|(時間があれば)アカウント登録|
|GET|/log/{user_id}|(時間があれば)今まで落とした城|


- GET /castles
Response:
```json
[
    {
    "id": 0,
    "name": "string",
    "summary": "string",
    "url": "string",
    "lat": 0,
    "lng": 0
  }
]
```
- 
