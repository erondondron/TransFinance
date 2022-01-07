from datetime import datetime
from typing import List

from pydantic import BaseModel
from tinvest import Candle as TCandle


class Candle(BaseModel):
    """
    Значения цен указаны в минимальных производных валюты (копейки, центы).
    Длительность свечи равна минуте.
    """
    open: int
    close: int
    high: int
    low: int
    value: int
    time: datetime

    @staticmethod
    def from_tinkoff_candle(t_candle: TCandle) -> "Candle":
        return Candle(
            open=int(t_candle.o * 100),
            close=int(t_candle.c * 100),
            high=int(t_candle.h * 100),
            low=int(t_candle.l * 100),
            value=t_candle.v,
            time=t_candle.time,
        )


class CandlesCollection(BaseModel):
    candles: List[Candle]
