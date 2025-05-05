"""
trade_processor.py
This module contains the TradeProcessor class, which is responsible for processing trades.
"""

from datetime import datetime
from typing import List, Dict
from uuid import uuid4

from base_trade import BaseTrade
from equity_trade import EquityTrade
from bond_trade import BondTrade
from derivative_trade import DerivativeTrade
from trade_factory import TradeFactory


class TradeProcessor:
    def __init__(self)-> None:
        # Dictionary to store trades
        self._trades = {}
    
    @property
    def trades(self)-> Dict[uuid4, BaseTrade]:
        return self._trades

    def add_trade(self, trade_details:Dict)-> None:
        trade_id = trade_details["trade_id"]
        
        if self.get_trade(trade_id):
            raise ValueError(f"Trade {trade_id} already exists. Try updating the trade instead.")
        
        trade_type = trade_details["trade_type"]
        if trade_type not in ["EQUITY", "BOND", "DERIVATIVE"]:
            raise ValueError(f"Invalid trade type: {trade_type}. Try 'EQUITY', 'BOND', or 'DERIVATIVE'.")
        
        trade = TradeFactory.create_trade(**trade_details)
        self.trades[trade_id] = trade

    def get_trade(self, trade_id:uuid4)-> BaseTrade:
        if trade_id not in self._trades:
            return None
        return self.trades[trade_id]

    # def update_trade(self, trade_id:uuid4, trade_details:Dict)-> None:
    #     trade = self.get_trade(trade_id)
    #     if not trade:
    #         raise ValueError(f"Trade {trade_id} does not exist. Try adding the trade instead.")
    #     trade.update_trade(trade_details)

    # def delete_trade(self, trade_id:uuid4)-> None:
    #     if trade_id not in self._trades:
    #         raise ValueError(f"Trade {trade_id} does not exist. Try adding the trade instead.")
    #     del self.trades[trade_id]

    def cancel_trade(self, trade_id:uuid4)-> None:
        trade = self.get_trade(trade_id)
        if not trade:
            raise ValueError(f"Trade {trade_id} does not exist. Cannot cancel if it doesn't exist.")
        
        if trade.status not in ["EXECUTED", "SETTLED"]:
            trade.status = "CANCELLED"
        else:
            raise ValueError(f"Trade {trade_id} is already executed or settled. Cannot be cancelled.")
        
    
    def validate_trade(self, trade: BaseTrade=None)-> None:
        if trade:
            errors = trade.validate_trade()
            if errors:
                self.cancel_trade(trade.trade_id)
                message = f"Trade {trade.trade_id} is invalid. Please check the trade details and try again."
            else:
                trade.transition_status(trade.status, "VALIDATED")
                message = f"Trade {trade.trade_id} is validated."
                
        else:
            message = "No trade provided to validate."
        
        return {
                "trade_id": trade.trade_id,
                "status": trade.status,
                "message": message
                }
        
    def execute_trade(self, trade: BaseTrade=None)-> None:
        if trade:
            trade.transition_status(trade.status, "EXECUTED")
        else:
            raise ValueError(f"Trade {trade.trade_id} does not exist. Cannot execute if it doesn't exist.")

    def settle_trade(self, trade: BaseTrade=None)-> None:
        if trade:
            trade.transition_status(trade.status, "SETTLED")
        else:
            raise ValueError(f"Trade {trade.trade_id} does not exist. Cannot settle if it doesn't exist.")


    def calculate_risk_exposure(self)-> Dict[str, float]:
        all_risk_exposures = 0
        equity_risk_exposures = 0
        bond_risk_exposures = 0
        derivative_risk_exposures = 0

        for trade in self.trades.values():
            risk_exposure = trade.calculate_risk()
            if trade.trade_type == "equity":
                equity_risk_exposures += risk_exposure
            elif trade.trade_type == "bond":
                bond_risk_exposures += risk_exposure
            else:
                derivative_risk_exposures += risk_exposure
            all_risk_exposures += risk_exposure

        return {
            "all_risk_exposures": all_risk_exposures,
            "equity_risk_exposures": equity_risk_exposures,
            "bond_risk_exposures": bond_risk_exposures,
            "derivative_risk_exposures": derivative_risk_exposures
        }

    def transition_trade_status(self, trade_id:uuid4, new_status:str)-> None:
        trade = self.get_trade(trade_id)
        if not trade:
            raise ValueError(f"Trade {trade_id} does not exist. Cannot transition status if it doesn't exist.")
        trade.transition_status(trade.status)

    def calculate_net_quantity(self, trade: BaseTrade)-> float:
        user_net_quantity = {}

        for trade in self.trades.values():
            if trade.user_id not in user_net_quantity:
                user_net_quantity[trade.user_id] = {}

            user_net_quantity[trade.user_id][trade.symbol] = user_net_quantity.get(trade.user_id, {}).get(trade.symbol, 0) \
                + trade.quantity if trade.direction == "BUY" else -trade.quantity

        return user_net_quantity
            
    def process_trades(self, trade_data:List[Dict])->None:
        for trade in trade_data:
            self.add_trade(trade)
    
        # validate the trades
        for trade in self.trades.values():
            self.validate_trade(trade)
        
        # execute the trades
        for trade in self.trades.values():
            self.execute_trade(trade)

        # settle the trades
        for trade in self.trades.values():
            self.settle_trade(trade)

        # calculate the risk exposure
        risk_exposure = self.calculate_risk_exposure()
        print(risk_exposure)


