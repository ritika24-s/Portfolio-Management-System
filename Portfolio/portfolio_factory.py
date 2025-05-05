from .base_portfolio import BasePortfolio
from .equity_portfolio import EquityPortfolio
from .fixed_income_portfolio import FixedIncomePortfolio
from .mixed_portfolio import MixedPortfolio


class PortfolioFactory:
    PORTFOLIOTYPES = {
        "EQUITY": EquityPortfolio,
        "FIXED_INCOME": FixedIncomePortfolio,
        "MIXED": MixedPortfolio,
    }

    def create_portfolio(self, portfolio_type:str, **kwargs)-> BasePortfolio:
        if portfolio_type not in PortfolioFactory.PORTFOLIOTYPES:
            raise ValueError("Invalid portfolio type")
        
        return PortfolioFactory.PORTFOLIOTYPES[portfolio_type](**kwargs)
