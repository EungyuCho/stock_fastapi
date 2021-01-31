from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Optional
from pykrx import stock
import datetime

app = FastAPI()


def getRecentDay():
    now = datetime.datetime.now()
    weekly = now.weekday()
    if weekly == 5:
        now = now - datetime.timedelta(1)
    elif weekly == 6:
        now = now - datetime.timedelta(2)
    return now.strftime('%Y%m%d')


@app.get('/stock/fdm',
         responses={
             200: {
                 "description": "전체 종목의 BPS/PER/PBR/ESP/DIV/DPS",
                 "content": {
                     "application/json": {
                         "example": {"data": [
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
                         ]}
                     }
                 },
             }
         })
async def fundamental_by_ticker(qDate: Optional[str] = None):
    date = getRecentDay()
    if qDate:
        date = qDate
    df = stock.get_market_fundamental_by_ticker(date)
    result = []
    df_arr = df.values
    df_index = df.index
    for i, data in enumerate(df_arr):
        if data[4] != 0:
            result.append({
                'ticker': df_index[i],
                'stock_name': data[0],
                'BPS': data[1],
                'PER': data[2],
                'PBR': data[3],
                'ESP': data[4],
                'DIV': data[5],
                'DPS': data[6]
            })
    return {
        "data": result
    }


@app.get('/index',
         responses={
             200: {
                 "description": "인덱스 전체 목록",
                 "content": {
                     "application/json": {
                         "example": {"data": [
                             {
                                 "1001": "코스피"
                             },
                             {
                                 "1002": "코스피 대형주"
                             },
                             {
                                 "1003": "코스피 중형주"
                             },
                             {
                                 "1004": "코스피 소형주"
                             },
                             {
                                 "1005": "음식료품"
                             },
                             {
                                 "1006": "섬유의복"
                             },
                             {
                                 "1007": "종이목재"
                             },
                             {
                                 "1008": "화학"
                             }
                         ]}
                     }
                 },
             }
         })
async def index_list(qDate: Optional[str] = None):
    result = []
    date = getRecentDay()
    if qDate:
        date = qDate
    for ticker in stock.get_index_ticker_list(date):
        result.append({
            ticker: stock.get_index_ticker_name(ticker)
        })
    return {
        "data": result
    }


@app.get('/index/{index_num}',
         responses={
             200: {
                 "description": "해당 인덱스에 포함되어있는 종목의 티커들",
                 "content": {
                     "application/json": {
                         "example": {
                             "data": [
                                 "086280",
                                 "003490",
                                 "011200",
                                 "180640",
                                 "000120",
                                 "336260",
                                 "012750",
                                 "047810",
                                 "028670",
                                 "006260",
                                 "012450",
                                 "047050",
                                 "010120",
                                 "272210",
                                 "001740",
                                 "051600",
                                 "020560",
                                 "001120",
                                 "000150",
                                 "079550"
                               ]
                         }
                     }
                 },
             }
         })
async def index_stock_list(index_num):
    df = stock.get_index_portfolio_deposit_file(index_num)
    return {
        "data": df
    }


@app.get('/fluctuation',
         responses={
             200: {
                 "description": "전체 종목 시세 조회 결과",
                 "content": {
                     "application/json": {
                         "example": {
                             "data": [
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
                               ]
                         }
                     }
                 },
             }
         })
async def fluctuation_stock_list(qDate: Optional[str] = None):
    date = getRecentDay()
    if qDate:
        date = qDate
    df = stock.get_market_ohlcv_by_ticker(date)
    result = []
    df_index = df.index
    df_arr = df._series
    start_price = df_arr.get('시가').values.tolist()
    highest_price = df_arr.get('고가').values.tolist()
    lowest_price = df_arr.get('저가').values.tolist()
    end_price = df_arr.get('종가').values.tolist()
    volume = df_arr.get('거래량').values.tolist()
    transaction_price = df_arr.get('거래대금').values.tolist()
    fluctuation_rate = df_arr.get('등락률').values.tolist()
    for i, index in enumerate(df_index):
        result.append({
            'ticker': index,
            'start_price': start_price[i],
            'highest_price': highest_price[i],
            'lowest_price': lowest_price[i],
            'end_price': end_price[i],
            'volume': volume[i],
            'transaction_price': transaction_price[i],
            'fluctuation_rate': fluctuation_rate[i]
        })
    return {
        'data': result,
    }


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stock_API - by Jay",
        version="1.0.0",
        description="with FastAPI",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi