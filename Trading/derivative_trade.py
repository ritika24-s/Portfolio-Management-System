"""
derivative_trade.py

This module contains the DerivativeTrade class, which is responsible for creating derivative trades.
"""
from datetime import datetime
from typing import Dict, List

from base_trade import BaseTrade


class DerivativeTrade(BaseTrade):
    """
    attributes:
        Underlying Symbol (e.g., "AAPL")
        Option Type (call/put)
        Strike Price
        Expiration Date
        Quantity (number of contracts)
        Premium (price paid per contract)
        Direction (buy/sell)
    """
    def __init__(self, trade_type:str, timestamp:datetime, status="NEW", trade_id:str=None, **kwargs)-> None:
        super().__init__(trade_type, timestamp, status, trade_id)
        self._underlying_symbol = kwargs.get("underlying_symbol")
        self._option_type = kwargs.get("option_type")
        self._strike_price = float(kwargs.get("strike_price", 0))
        self._expiration_date = datetime.strptime(kwargs.get("expiration_date"), "%Y-%m-%d")
        self._quantity = int(kwargs.get("quantity", 0))
        self._premium = float(kwargs.get("premium", 0))
    
    @property
    def underlying_symbol(self)-> str:
        return self._underlying_symbol

    @underlying_symbol.setter
    def underlying_symbol(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("underlying_symbol must be a string")
        self._underlying_symbol = value
    
    @property
    def option_type(self)-> str:
        return self._option_type

    @option_type.setter
    def option_type(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("option_type must be a string")
        self._option_type = value

    @property
    def strike_price(self)-> float:
        return self._strike_price
    
    @strike_price.setter
    def strike_price(self, value:float)-> None:
        if not isinstance(value, float):
            raise ValueError("strike_price must be a float")
        self._strike_price = value
    
    @property 
    def expiration_date(self)-> datetime:
        return self._expiration_date
    
    @expiration_date.setter
    def expiration_date(self, value:datetime)-> None:
        if not isinstance(value, datetime):
            raise ValueError("expiration_date must be a datetime")
        self._expiration_date = value
    
    @property
    def quantity(self)-> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value:int)-> None:
        if not isinstance(value, int):
            raise ValueError("quantity must be an integer")
        self._quantity = value
    
    @property
    def premium(self)-> float:
        return self._premium
    
    @premium.setter
    def premium(self, value:float)-> None:
        if not isinstance(value, float):
            raise ValueError("premium must be a float")
        self._premium = value    

    def validate_trade(self)-> Dict[str, bool| List[str]]:
        """
        Verify strike price is positive, expiration date is in the future, premium is non-negative
        """
        validation_errors = []
        if self.strike_price <= 0:
            validation_errors.append("Strike price must be positive")
        if self.expiration_date <= datetime.now() or self.expiration_date is None:
            validation_errors.append("Expiration date must be in the future")
        if self.premium < 0:
            validation_errors.append("Premium must be non-negative")

        if validation_errors:
            return validation_errors
        else:
            return True
            
    def calculate_risk(self)-> float:
        """
        Calculate the risk of the trade
        """
        # Calculate simple delta exposure (0.5 × strike price × quantity for calls, -0.5 × strike price × quantity for puts)
        return 0.5 * self.strike_price * self.quantity if self.option_type == "call" else -0.5 * self.strike_price * self.quantity
