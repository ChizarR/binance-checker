#!/usr/bin/env python

from datetime import datetime
import json

from websocket import WebSocketApp


BASE_URL = "wss://fstream.binance.com/ws/"


def on_open(_: WebSocketApp) -> None:
    print("Connection open")


def on_ping(_: WebSocketApp) -> None:
    print("Got a ping!")


def on_message(_: WebSocketApp, msg) -> None:
    parsed_msg = json.loads(msg)

    time = int(parsed_msg["E"])
    pair = parsed_msg["s"]
    curr_open_price = float(parsed_msg["k"]["o"])
    curr_high_price = float(parsed_msg["k"]["h"])

    change = _count_price_change(curr_open_price, curr_high_price)
    if change <= 0.99:
        _print_info_msg(pair, curr_open_price, curr_high_price, change, time)


def on_close(_: WebSocketApp, status, message) -> None:
    print("\nConnection closed")


def _count_price_change(curr_price: float, max_price: float) -> float:
    return curr_price / max_price


def _print_info_msg(pair: str, curr_price: float,
                    max_price: float, change: float, time: int) -> None:
    print("--------------------------------------------------")
    print(f"Time: {_convert_unix_time(time)}"
          f"Pair: {pair}\n"
          f"The price fell by {change}% from the maximum.\n"
          f"Open price: {curr_price}; Max price: {max_price}")


def _convert_unix_time(time: int) -> str:
    t = datetime.fromtimestamp(time / 1000)
    return t.strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    url = f"{BASE_URL}xrpusdt@kline_1h"
    ws = WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,
    )
    ws.run_forever(suppress_origin=True)


if __name__ == "__main__":
    try:
        print("START SCRIPT")
        main()
    except KeyboardInterrupt:
        print("SCRIPT STOPPED")
