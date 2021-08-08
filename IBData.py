from typing import Union
from typing import List
from enum import Enum
from session import InteractiveBrokersSession

class Accounts():
    def __init__(self, ib_session: InteractiveBrokersSession):
        self.session = ib_session
        self._has_portfolio_been_called = False
        self._has_sub_portfolio_been_called = False

    def accounts(self) -> dict:
        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/accounts'
        )
        return content


class PortfolioAccounts():
    def __init__(self, ib_session: InteractiveBrokersSession):
        self.session: InteractiveBrokersSession = ib_session
        self._has_portfolio_been_called = False
        self._has_sub_portfolio_been_called = False

    def accounts(self) -> list:
        content = self.session.make_request(
            method='get',
            endpoint='/api/portfolio/accounts'
        )

        self._has_portfolio_been_called = True
        return content

    def subaccounts(self) -> list:
        content = self.session.make_request(
            method='get',
            endpoint='/api/portfolio/subaccounts'
        )

        self._has_sub_portfolio_been_called = True

        return content

    def account_metadata(self, account_id: str) -> dict:
        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/meta'
        )

        return content

    def account_summary(self, account_id: str) -> dict:
        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/summary'
        )

        return content

    def portfolio_allocation(self, account_ids: List[str]) -> dict:

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        payload = {
            'acctIds': account_ids
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/portfolio/allocation',
            json_payload=payload
        )

        return content

    def portfolio_positions(self, account_id: str, page_id: int = 0, sort: Union[str, Enum] = None,
        direction: Union[str, Enum] = None, period: str = None) -> dict:
        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        if isinstance(sort, Enum):
            sort = sort.value

        if isinstance(direction, Enum):
            direction = direction.value

        params = {
            'sort': sort,
            'direction': direction,
            'period': period
        }

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/portfolio/{account_id}/positions/{page_id}',
            params=params
        )

        return content

class Contracts():
    def __init__(self, ib_session: InteractiveBrokersSession) :
        self.session: InteractiveBrokersSession = ib_session

    def contract_info(self, contract_id: str) -> dict:
        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/contract/{contract_id}/info'
        )

        return content

    def search_symbol(self, symbol: str, name: str = False, security_type: str = None) -> list:
        payload = {
            'symbol': symbol,
            'name': name,
            'secType': security_type
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/secdef/search',
            json_payload=payload
        )

        return content

class MarketData():

    def __init__(self, ib_session: InteractiveBrokersSession) -> None:
        self.session = ib_session

    def snapshot(self, contract_ids: List[str], since: int = None, fields: Union[str, Enum] = None) -> dict:
        new_fields = []

        if fields:
            # Check for Enums.
            for field in fields:

                if isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

            fields = ','.join(new_fields)
        else:
            fields = None

        # Define the payload.
        params = {
            'conids': ','.join(contract_ids),
            'since': since,
            'fields': fields
        }

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/marketdata/snapshot',
            params=params
        )

        return content

    def market_history(self, contract_id: str, period: str, bar: Union[str, Enum] = None,
            exchange: str = None, outside_regular_trading_hours: bool = True) -> dict:

        if isinstance(bar, Enum):
            bar = bar.value

        payload = {
            'conid': contract_id,
            'period': period,
            'bar': bar,
            'exchange': exchange,
            'outsideRth': outside_regular_trading_hours
        }

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/marketdata/history',
            params=payload
        )

        return content
