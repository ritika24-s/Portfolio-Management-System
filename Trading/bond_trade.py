from datetime import datetime
from typing import Dict, List
from base_trade import BaseTrade


class BondTrade(BaseTrade):
    """
    attributes:
        ISIN (International Securities Identification Number)
        Face Value (nominal amount)
        Price (as percentage of face value)
        Coupon Rate (annual interest rate)
        Maturity Date (when bond expires)
        Issuer (e.g., "US Treasury", "Apple Inc")
        Direction (buy/sell)
    """
    def __init__(self, trade_type:str, timestamp:datetime, status="NEW", trade_id:str=None, **kwargs)-> None:
        super().__init__(trade_type, timestamp, status, trade_id)
        self._isin = kwargs.get("isin")
        self._face_value = int(kwargs.get("face_value"))
        self._price = float(kwargs.get("price"))
        self._coupon_rate = float(kwargs.get("coupon_rate"))
        self._maturity_date = datetime.strptime(kwargs.get("maturity_date"), "%Y-%m-%d")
        self._issuer = kwargs.get("issuer")
        self._direction = kwargs.get("direction")

    @property
    def isin(self)-> str:
        return self._isin
    
    @isin.setter
    def isin(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("ISIN must be a string")
        self._isin = value
    
    @property
    def face_value(self)-> float:
        return self._face_value 
    
    @face_value.setter
    def face_value(self, value:float)-> None:
        if not isinstance(value, float) or value <= 0:
            raise ValueError("Face value must be a positive float")
        self._face_value = value
    
    @property
    def price(self)-> float:
        return self._price
    
    @price.setter
    def price(self, value:float)-> None:
        if not isinstance(value, float) or value < 0:
            raise ValueError("Price must be a positive float")
        self._price = value

    @property
    def coupon_rate(self)-> float:
        return self._coupon_rate
    
    @coupon_rate.setter
    def coupon_rate(self, value:float)-> None:
        if not isinstance(value, float) or value < 0 or value > 15:
            raise ValueError("Coupon rate must be a float between 0 and 15")
        self._coupon_rate = value
    
    @property
    def maturity_date(self)-> datetime:
        return self._maturity_date

    @maturity_date.setter

    @property
    def issuer(self)-> str:
        return self._issuer
    
    @issuer.setter
    
    @property
    def direction(self)-> str:
        return self._direction
    
    @direction.setter
    def direction(self, value:str)-> None:
        if not isinstance(value, str):
            raise ValueError("Direction must be a string")    
    
    def validate_trade(self)-> Dict[str, bool| List[str]]:
        """
        Verify face value is positive, coupon rate is between 0-15%, maturity date is in the future
        """
        validation_errors = []
        if not isinstance(self.face_value, float) or self.face_value <= 0:
            validation_errors.append("Face value must be positive")
        
        if not isinstance(self.coupon_rate, float) or self.coupon_rate <= 0 or self.coupon_rate >= 15:
            validation_errors.append("Coupon rate must be between 0 and 15")

        if not isinstance(self.maturity_date, datetime) or self.maturity_date <= datetime.now():
            validation_errors.append("Maturity date must be in the future")

        if validation_errors:
            return validation_errors
        else:
            return True

    def calculate_risk(self)-> float:
        maturity_year = self.maturity_date.year
        current_year = datetime.now().year
        years_to_maturity = maturity_year - current_year
        return self.face_value * self.price * years_to_maturity


