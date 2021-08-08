from enum import Enum
from os import close

class AccountInfo(Enum):
    AccountId = 1
    AccountTitle = 2

def account_info_key_to_string(account_info: AccountInfo):
    return {
        AccountInfo.AccountId : 'accountId',
        AccountInfo.AccountTitle : 'accountTitle'
    }[account_info]

class PositionInfo(Enum):
    AssertClass = 1
    ContractDescription = 2
    MarketPrice = 3
    MarketValue = 4
    Poistion = 5
    RealizedPL = 6
    UnrealizedPL = 7

    UnderlyingOpenPrice = 8
    UnderlyingClosePrice = 9

def position_info_key_to_string(position_info: PositionInfo):
    return {
        PositionInfo.AssertClass : 'assetClass',
        PositionInfo.ContractDescription : 'contractDesc',
        PositionInfo.MarketPrice : 'mktPrice',
        PositionInfo.MarketValue : 'mktValue',
        PositionInfo.Poistion : 'position',
        PositionInfo.RealizedPL : 'realizedPnl',
        PositionInfo.UnrealizedPL : 'unrealizedPnl'
    }[position_info]

class MarketDataInfo(Enum):
    BarLength = 1
    Data = 2
    Symbol = 3

def market_data_info_key_to_string(market_data_info: MarketDataInfo):
    return {
        MarketDataInfo.BarLength : 'barLength',
        MarketDataInfo.Data : 'data',
        MarketDataInfo.Symbol : 'symbol'
    }[market_data_info]

class PriceInfo(Enum):
    High = 1
    Low = 2
    Open = 3
    Close = 4

def price_info_key_to_string(price_info: PriceInfo):
    return {
        PriceInfo.High : 'h',
        PriceInfo.Low : 'l',
        PriceInfo.Open : 'o',
        PriceInfo.Close : 'c'
    }[price_info]