"""
base_trade.py

This module contains the base class for all trades.
"""
from abc import ABC, abstractmethod
from uuid import uuid4
from datetime import datetime
from typing import List, Dict
from enum import Enum


class TradeStatus(Enum):
    NEW = "NEW"
    VALIDATED = "VALIDATED"
    EXECUTED = "EXECUTED"
    SETTLED = "SETTLED"
    CANCELLED = "CANCELLED"


class BaseTrade(ABC):
    STATUS = {
        TradeStatus.NEW: [TradeStatus.VALIDATED],
        TradeStatus.VALIDATED: [TradeStatus.EXECUTED, TradeStatus.CANCELLED],
        TradeStatus.EXECUTED: [TradeStatus.SETTLED, TradeStatus.CANCELLED],
        TradeStatus.SETTLED: []
    }

    def __init__(self, trade_type:str, timestamp:datetime, status=TradeStatus.NEW, trade_id:str=None)-> None:
        self._trade_type = trade_type
        self._timestamp = timestamp
        self._status = status
        self.trade_id = trade_id

    @property
    def trade_type(self)-> str:
        return self._trade_type
    
    @trade_type.setter
    def trade_type(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("trade_type must be a string")
        self._trade_type = value

    @property
    def timestamp(self)-> datetime:
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value:datetime)-> None:
        if not isinstance(value, datetime): 
            raise ValueError("timestamp must be a datetime")
        self._timestamp = value

    @property
    def status(self)-> str:
        try:
            return self._status.value
        except AttributeError as e:
            print(e)


    @status.setter
    def status(self, value:str)-> None:
        try:
            enum_value = TradeStatus(value)
            if enum_value not in self.STATUS:
                raise ValueError("status must be one of the following: {}".format(TradeStatus))
            self._status = value
        except ValueError as e:
            print(e)

    @abstractmethod
    def validate_trade(self, *args, **kwargs)-> Dict[str, bool| List[str]]:
        pass

    @abstractmethod
    def calculate_risk(*args, **kwargs)-> float:
        pass

    def transition_status(self, current_status:str, new_status:str="")-> str:
        try:
            current_status = TradeStatus(current_status)
            if new_status:
                new_status = TradeStatus(new_status)
                if new_status not in self.STATUS[current_status]:
                    raise ValueError("Invalid new status")
            else:
                new_status = self.STATUS[current_status][0]
            self.status = TradeStatus(new_status)
            return new_status
        except ValueError as e:
            print(e)

    def __str__(self)-> str:
        return f"Trade Type: {self.trade_type}, ID: {self.id}, Timestamp: {self.timestamp}, Status: {self.status}"














