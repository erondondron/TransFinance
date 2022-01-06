from datetime import datetime

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
            int(t_candle.o * 100),
            int(t_candle.c * 100),
            int(t_candle.h * 100),
            int(t_candle.l * 100),
            t_candle.v,
            t_candle.time,
        )
