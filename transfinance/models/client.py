from datetime import datetime
from typing import List

from tinvest import (
    SyncClient,
    SandboxRegisterRequest,
    BrokerAccountType,
    MarketInstrument,
    CandleResolution,
    Candle as TCandle,
)

from transfinance.models.candle import Candle
from transfinance.settings import Settings


class TinkoffClient:
    sync = SyncClient(Settings.TINKOFF_SANDBOX_TOKEN, use_sandbox=True)

    @staticmethod
    def register_broker() -> str:
        broker_type = BrokerAccountType.tinkoff
        req = SandboxRegisterRequest(broker_account_type=broker_type)
        resp = TinkoffClient.sync.register_sandbox_account(req)
        broker_id: str = resp.payload.broker_account_id
        return broker_id

    @staticmethod
    def clear_all_brokers() -> None:
        brokers = TinkoffClient.sync.get_accounts().payload.accounts
        for b in brokers:
            TinkoffClient.sync.clear_sandbox_account(b.broker_account_id)
            TinkoffClient.sync.remove_sandbox_account(b.broker_account_id)

    @staticmethod
    def get_candles(
        figi: str,
        from_dt: datetime,
        to_dt: datetime,
        resolution: CandleResolution,
    ) -> List[Candle]:
        resp = TinkoffClient.sync.get_market_candles(
            figi, from_dt, to_dt, resolution
        )
        t_candles: List[TCandle] = resp.payload.candles
        candles: List[Candle] = list(map(Candle.from_tinkoff_candle, t_candles))
        return candles

    @staticmethod
    def get_market_stocks() -> List[MarketInstrument]:
        resp = TinkoffClient.sync.get_market_stocks()
        stocks: List[MarketInstrument] = resp.payload.instruments
        return stocks

    @staticmethod
    def dump_market_stocks() -> None:
        stocks = [
            f"{s.name} ({s.currency.value}): {s.figi}"
            for s in TinkoffClient.get_market_stocks()
        ]
        with open(Settings.FIGI_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(stocks))
