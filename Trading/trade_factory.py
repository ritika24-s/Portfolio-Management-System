"""
trade_factory.py

This module contains the TradeFactory class, which is responsible for creating trades.
"""

from datetime import datetime
from uuid import uuid4

from base_trade import BaseTrade
from equity_trade import EquityTrade
from bond_trade import BondTrade
from derivative_trade import DerivativeTrade

class TradeFactory:
    TRADETYPES = {
        "EQUITY": EquityTrade,
        "BOND": BondTrade,
        "DERIVATIVE": DerivativeTrade,
    }

    @staticmethod
    def create_trade(trade_type:str="", **kwargs)-> BaseTrade:
        if trade_type not in TradeFactory.TRADETYPES:
            raise ValueError("Invalid trade type")

        if "timestamp" not in kwargs:
            kwargs["timestamp"] = datetime.now()
        if "trade_id" not in kwargs:
            kwargs["trade_id"] = str(uuid4())
        if "trade_type" not in kwargs:
            kwargs["trade_type"] = trade_type

        return TradeFactory.TRADETYPES[trade_type](**kwargs)
