# STOCK-API

## Use
<p>
<img src="https://img.shields.io/badge/-Python-3776AB?&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/-FastAPI-009688?&logo=FastAPI&logoColor=white"/></a>
</p>

<a href="https://github.com/sharebook-kr/pykrx/tree/ec5ef7b437f8538f57dea3c80c9ce6ee9c5e6958">PyKrx Library</a> 

## API LIST

### 종목별 BPS/PER/PBR/ESP/DIV/DSP 조회
<pre><code>Request: /stock/fdm
Method: GET
Response:
{
    data: [
        {
            "ticker": "095570",
            "stock_name": "AJ네트웍스 ",
            "BPS": 6802,
            "PER": 4.078125,
            "PBR": 0.5887560643928257,
            "ESP": 982,
            "DIV": 7.48046875,
            "DPS": 300
        },
        {
            "ticker": "006840",
            "stock_name": "AK홀딩스 ",
            "BPS": 62448,
            "PER": 13.3515625,
            "PBR": 0.46352465251088903,
            "ESP": 2168,
            "DIV": 2.58984375,
            "DPS": 750
        },
        ...
    ]
}
</code></pre>

### 인덱스 목록 조회
<pre><code>Request: /index
Method: GET
Response:
{
    data: [
        {
            "1001": "코스피"
        },
        {
            "1002": "코스피 대형주"
        },
        ...
    ]
}
</code></pre>

### 인덱스 구성종목 검색
<pre><code>Request: /index/{index_num}
Method: GET
Response:
{
    data: [
        "086280",
        "003490",
        "011200",
        ...
    ]
}
</code></pre>

### 전체 시세 조회
<pre><code>Request: /fluctuation
Method: GET
Response:
{
    data: [
        {
            "ticker": "095570",
            "start_price": 5410,
            "highest_price": 5520,
            "lowest_price": 5360,
            "end_price": 5370,
            "volume": 39296,
            "transaction_price": 211983170,
            "fluctuation_rate": -3.419921875
        },
        {
            "ticker": "068400",
            "start_price": 10300,
            "highest_price": 10450,
            "lowest_price": 10100,
            "end_price": 10200,
            "volume": 109070,
            "transaction_price": 1117805500,
            "fluctuation_rate": -1.919921875
        },
        ...
    ]
}
</code></pre>

## Running the app
<pre><code>$ uvicorn index:app</code></pre>
<blockquote>App will be run on 127.0.0.1:8000<br>
You can see API Docs at <a href="http://127.0.0.1:8000/redoc">here</a></blockquote>