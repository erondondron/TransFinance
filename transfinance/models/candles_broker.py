import itertools
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from transfinance.models.candle import CandlesCollection
from transfinance.settings import Settings


class CandlesBroker:
    def __init__(self, figi: str) -> None:
        self._figi: str = figi
        self._figi_dir = Settings.CANDLES_DIR.joinpath(figi)

    def empty(self) -> bool:
        return not bool(next(self._figi_dir.iterdir(), None))

    def dump_candles(self, collection: CandlesCollection) -> None:
        yearly_candles = defaultdict(list)
        for candle in collection:
            yearly_candles[candle.time.year].append(candle)
        for year, candles in yearly_candles.items():
            self._dump_candles_by_year(CandlesCollection(candles=candles), year)

    def get_candles(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> Optional[CandlesCollection]:
        yearly = [
            self._get_candles_by_year(year).candles
            for year in range(start.year, end.year + 1)
        ]
        yearly[0] = [c for c in yearly[0] if c.time >= start]
        yearly[-1] = [c for c in yearly[-1] if c.time <= end]
        candles_iter = itertools.chain.from_iterable(yearly)
        return CandlesCollection(candles=list(candles_iter))

    def update(self) -> None:
        pass

    def _dump_candles_by_year(
        self, candles: CandlesCollection, year: int
    ) -> None:
        file_path = self._figi_dir.joinpath(f"{year}.json")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(candles.json())

    def _get_candles_by_year(self, year: int) -> Optional[CandlesCollection]:
        file_path = self._yearly_candles_path(year)
        if not file_path.exists():
            return
        return CandlesCollection.parse_file(file_path)

    def _yearly_candles_path(self, year: int) -> Path:
        return self._figi_dir.joinpath(f"{year}.json")
