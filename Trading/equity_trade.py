"""
equity_trade.py

"""
from datetime import datetime
from typing import Dict, List   
from base_trade import BaseTrade


class EquityTrade(BaseTrade):
    def __init__(self, trade_type:str, timestamp:datetime, status="NEW", trade_id:str=None, **kwargs)-> None:
        super().__init__(trade_type, timestamp, status, trade_id)
        self._symbol = kwargs.get("symbol")
        self._quantity = float(kwargs.get("quantity"))
        self._price = float(kwargs.get("price"))
        self._direction = kwargs.get("direction")
        self._market = kwargs.get("market")

    @property
    def symbol(self)-> str:
        return self._symbol
    
    @symbol.setter
    def symbol(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("Symbol must be a string")
        self._symbol = value
    
    @property
    def quantity(self)-> float:
        return self._quantity  

    @quantity.setter
    def quantity(self, value:float)-> None:
        if not isinstance(value, float) or value < 0:
            raise ValueError("Quantity must be a positive float")
        self._quantity = value
    
    @property
    def price(self)-> float:
        return self._price
    
    @price.setter
    def price(self, value:float)-> None:
        if not isinstance(value, float) or value < 0:
            raise ValueError("Price must be a positive float")
        self._price = value

    @property
    def direction(self)-> str:
        return self._direction
    
    @direction.setter
    def direction(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("Direction must be a string")
        
    @property
    def market(self)-> str:
        return self._market
    
    @market.setter
    def market(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("Market must be a string")

    def validate_trade(self)-> Dict[str, bool|List[str]]:
        validation_errors = []
        if not isinstance(self.symbol, str) and self.symbol is not None:
            validation_errors.append("Symbol must be a string")
        if self.quantity is not None and (not isinstance(self.quantity, float) or self.quantity < 0):
            validation_errors.append("Quantity must be positive")
        if self.price is not None and (not isinstance(self.price, float) or self.price < 0):
            validation_errors.append("Price must be positive")
        
        if not validation_errors:
            return True
        else:
            return validation_errors

    def calculate_risk(self)-> float:
        return self.price * self.quantity * 0.08

    

