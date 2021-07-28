from __future__ import print_function
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
import asyncio
import json
import sys

ALPACA_API_KEY = ""
ALPACA_SECRET_KEY = ""

data = []
with open('stock_list.txt', 'r') as filestream:
    # Read all lines in the file one by one
    for line in filestream:
        data.append({'symbol': line})
filestream.close()

with open('data.json', 'w') as jsonfile:
    json.dump(data, jsonfile)
jsonfile.close()

with open('data.json') as jsonfile:
    stock_data = json.load(jsonfile)
jsonfile.close()

arr = []

for s in stock_data:
    stock = s['symbol'].strip()
    arr.append(stock)

stock_tuple = tuple(arr)

async def print_quote(q):
    print('quote', q)


def consumer_thread():
    global conn
    conn = Stream(ALPACA_API_KEY,
                  ALPACA_SECRET_KEY,
                  base_url=URL('https://paper-api.alpaca.markets'),
                  data_stream_url=URL('wss://stream.data.alpaca.markets'),
                  data_feed='sip')

    conn.subscribe_quotes(print_quote, *stock_tuple)
    conn.run()


loop = asyncio.get_event_loop()
loop.call_soon(consumer_thread())