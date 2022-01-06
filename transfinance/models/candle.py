from datetime import datetime

from tinvest import Candle as TCandle


class Candle:
    """
    Значения цен указаны в минимальных производных валюты (копейки, центы)
    """

    def __init__(
        self, o: int, c: int, h: int, l: int, v: int, t: datetime
    ) -> None:
        self._open: int = o
        self._close: int = c
        self._high: int = h
        self._low: int = l
        self._value: int = v
        self._time: datetime = t

    @property
    def open_price(self) -> int:
        return self._open

    @property
    def close_price(self) -> int:
        return self._close

    @property
    def high_price(self) -> int:
        return self._high

    @property
    def low_price(self) -> int:
        return self._low

    @property
    def value(self) -> int:
        return self._value

    @property
    def time(self) -> datetime:
        return self._time

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
