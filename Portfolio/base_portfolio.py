"""
portfolio.py
"""
from abc import ABC, abstractmethod
from datetime import datetime


class BasePortfolio(ABC):
    def __init__(self, position, rebalance, instrument, quantity, currency_type, price, value, timestamp, trade_id, transaction_id):
        self._position = position
        self._rebalance = rebalance
        self._instrument = instrument
        self._quantity = quantity
        self.average_cost = 0.0
        self._currency_type = currency_type
        self._price = price
        self._timestamp = timestamp if timestamp else datetime.now()
        self._trade_id = trade_id
        self._transaction_id = transaction_id
        self._monthy_returns = 0
        self._daily_returns = 0
    
    @abstractmethod
    def add_position(self, position):
        pass

    @abstractmethod
    def remove_position(self, position):
        pass
    
    @abstractmethod
    def add_rebalance(self, rebalance):
        pass

    @abstractmethod
    def remove_rebalance(self, rebalance):
        pass
