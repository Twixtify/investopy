from typing import Callable

from calculators.approx_portfolio import ApproxPortfolio
from calculators.min_portfolio_investment import MinPortfolio
from .commands import IBIndex
from .portfolio import Portfolio
from .portfolio_receiver import IBIndexOperation

PortfolioSurveyStrategy = Callable[[float], Portfolio]


def ibindex_strategy(deposit: float) -> Portfolio:
    calculator = ApproxPortfolio(deposit,
                                 stocks_to_exclude=['Havsfrun Investment B',
                                                    'NAXS',
                                                    'Traction B',
                                                    'Öresund',
                                                    'Karolinska Development B',
                                                    'VEF',
                                                    'Fastator',
                                                    'VNV Global',
                                                    'Linc']
                                 )
    receiver = IBIndexOperation(calculator)
    return IBIndex(deposit, receiver)


def min_ibindex_strategy(deposit: float) -> Portfolio:
    calculator = MinPortfolio(deposit,
                              stocks_to_exclude=['Havsfrun Investment B',
                                                 'NAXS',
                                                 'Traction B',
                                                 'Öresund',
                                                 'Karolinska Development B',
                                                 'VEF',
                                                 'Fastator',
                                                 'VNV Global']
                              )
    receiver = IBIndexOperation(calculator)
    return IBIndex(deposit, receiver)
