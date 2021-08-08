from IBDataManager import IBDataManager
from DataInfo import *
import csv
import datetime

class CSVCreator:
    def __init__(self) -> None:
        self._dataManager = IBDataManager()

    def create_files_with_positions(self, include_underlying_prices_for_options=False):
        accounts = self._dataManager.get_accounts_info([AccountInfo.AccountId, AccountInfo.AccountTitle])
        for account in accounts:
            needed_info = [PositionInfo.ContractDescription, PositionInfo.AssertClass, PositionInfo.Poistion,
                PositionInfo.MarketPrice, PositionInfo.MarketValue, PositionInfo.RealizedPL, PositionInfo.UnrealizedPL]
            positions = self._dataManager.get_positions_for_account(account, needed_info)

            if include_underlying_prices_for_options:
                needed_info.append(PositionInfo.UnderlyingOpenPrice)
                needed_info.append(PositionInfo.UnderlyingClosePrice)
                self._add_underlying_prices_for_options(positions=positions)

            with open(f'{self._create_file_name(account)}.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([self._info_value_to_column_name(value) for value in needed_info])
                for position in positions:
                    writer.writerow([value for value in position.values()])

    def _add_underlying_prices_for_options(self, positions):
        for position in positions:
            if position[PositionInfo.AssertClass] != 'OPT':
                continue
            prices = self._dataManager.get_last_prices_for_symbol(
                self._get_underlying_symbol_from_option_name(position[PositionInfo.ContractDescription]),
                info_keys=[PriceInfo.Open, PriceInfo.Close])

            position[PositionInfo.UnderlyingOpenPrice] = prices[0][PriceInfo.Open]
            position[PositionInfo.UnderlyingClosePrice] = prices[0][PriceInfo.Close]

    def _get_underlying_symbol_from_option_name(self, option_name):
        return option_name.split(' ')[0]

    def _create_file_name(self, account):
        title = account[AccountInfo.AccountTitle]
        return f'{title}_{datetime.datetime.now().date()}'        

    def _info_value_to_column_name(self, position_key):
        return {
            PositionInfo.AssertClass : 'Type',
            PositionInfo.ContractDescription : 'Contract',
            PositionInfo.MarketPrice : 'Market Price',
            PositionInfo.MarketValue : 'Market Value',
            PositionInfo.Poistion : 'Poistion',
            PositionInfo.RealizedPL : 'Realized P/L',
            PositionInfo.UnrealizedPL : 'Unrealized P/L',
            PositionInfo.UnderlyingOpenPrice : 'Underlying Open Price',
            PositionInfo.UnderlyingClosePrice : 'Underlying Close Price',
        }[position_key]
    