from session import InteractiveBrokersSession
from IBData import *
from Enums import BarType
from DataInfo import *
from pprint import pprint
import csv 

class IBDataManager:
    def __init__(self) -> None:
        self.ib_session = InteractiveBrokersSession()
        self.accounts_service = Accounts(ib_session=self.ib_session)
        self.portfolio_accounts_service = PortfolioAccounts(ib_session=self.ib_session)
        self.contracts_service = Contracts(ib_session=self.ib_session)
        self.market_data_service = MarketData(ib_session=self.ib_session)

    def get_accounts_info(self, info_keys):
        accounts = self.portfolio_accounts_service.accounts()
        return self._create_result_info(accounts, info_keys, account_info_key_to_string)

    def get_positions_for_account(self, account_info, info_keys):
        account_positions = self.portfolio_accounts_service.portfolio_positions(account_info[AccountInfo.AccountId])
        return self._create_result_info(account_positions, info_keys, position_info_key_to_string)

    def get_market_data_for_symbol(self, symbol, info_keys, period):
        symbol_info = self.contracts_service.search_symbol(symbol=symbol)
        contract_id = symbol_info[0]['conid']
        market_data =  self.market_data_service.market_history(contract_id=contract_id,
            period=period.value, bar=period)
        return self._create_result_info([market_data], info_keys, market_data_info_key_to_string)

    def get_last_prices_for_symbol(self, symbol, info_keys):
        data = self.get_market_data_for_symbol(symbol, [MarketDataInfo.Data], BarType.OneDay)
        return self._create_result_info(data[0][MarketDataInfo.Data], info_keys, price_info_key_to_string)
        
    def _create_result_info(self, values_from_server, keys, transform_function):
        result_info = []
        for value_from_server in values_from_server:
            value_info = {}
            for key in keys:
                value_info[key] = value_from_server[transform_function(key)]
            result_info.append(value_info)
        return result_info
