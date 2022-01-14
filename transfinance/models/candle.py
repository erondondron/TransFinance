from datetime import datetime
from typing import List, Iterator

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

    def __iter__(self) -> Iterator:
        return iter(self.candles)

    def __getitem__(self, item: int) -> Candle:
        return self.candles[item]

    def __setslice__(
        self, start: int, end: int, step: int
    ) -> "CandlesCollection":
        return CandlesCollection(candles=self.candles[start:end:step])

    def sort(self) -> None:
        self.candles = list(sorted(self.candles, key=lambda c: c.time))

    def last_date(self) -> datetime:
        last_candle = max(self.candles, key=lambda c: c.time)
        return last_candle.time

    def first_date(self) -> datetime:
        first_candle = min(self.candles, key=lambda c: c.time)
        return first_candle.time
