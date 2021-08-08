from enum import Enum

class BarType(Enum):
    OneMinute = '1min'
    TwoMinute = '2min'
    ThreeMinute = '3min'
    FiveMinute = '5min'
    TenMinute = '10min'
    FifteenMinute = '15min'
    ThirtyMinute = '30min'
    OneHour = '1h'
    TwoHour = '2h'
    ThreeHour = '3h'
    FourHour = '4h'
    EightHour = '8h'
    OneDay = '1d'
    OneWeek = '1w'
    OneMonth = '1m'