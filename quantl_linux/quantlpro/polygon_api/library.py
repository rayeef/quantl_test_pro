from polygon_api.definitions import LastTrade
from polygon_api.definitions import LastQuote
from polygon_api.definitions import HistTrade
from polygon_api.definitions import Quote
from polygon_api.definitions import Aggregate
from polygon_api.definitions import Company
from polygon_api.definitions import CompanyV3
from polygon_api.definitions import Address
from polygon_api.definitions import Symbol
from polygon_api.definitions import SymbolV3
from polygon_api.definitions import Dividend
from polygon_api.definitions import News
from polygon_api.definitions import NewsV2
from polygon_api.definitions import Publisher
from polygon_api.definitions import Earning
from polygon_api.definitions import Financial
from polygon_api.definitions import Exchange
from polygon_api.definitions import Error
from polygon_api.definitions import NotFound
from polygon_api.definitions import Conflict
from polygon_api.definitions import Unauthorized
from polygon_api.definitions import MarketStatus
from polygon_api.definitions import MarketHoliday
from polygon_api.definitions import AnalystRatings
from polygon_api.definitions import RatingSection
from polygon_api.definitions import CryptoTick
from polygon_api.definitions import CryptoTickJson
from polygon_api.definitions import CryptoExchange
from polygon_api.definitions import CryptoSnapshotTicker
from polygon_api.definitions import CryptoSnapshotBookItem
from polygon_api.definitions import CryptoSnapshotTickerBook
from polygon_api.definitions import CryptoSnapshotAgg
from polygon_api.definitions import Forex
from polygon_api.definitions import LastForexTrade
from polygon_api.definitions import LastForexQuote
from polygon_api.definitions import ForexAggregate
from polygon_api.definitions import ForexSnapshotTicker
from polygon_api.definitions import ForexSnapshotAgg
from polygon_api.definitions import Ticker
from polygon_api.definitions import Split
from polygon_api.definitions import Financials
from polygon_api.definitions import Trade
from polygon_api.definitions import StocksSnapshotTicker
from polygon_api.definitions import StocksSnapshotBookItem
from polygon_api.definitions import StocksSnapshotTickerBook
from polygon_api.definitions import StocksV2Trade
from polygon_api.definitions import StocksV2NBBO
from polygon_api.definitions import StocksSnapshotAgg
from polygon_api.definitions import StocksSnapshotQuote
from polygon_api.definitions import Aggv2
from polygon_api.definitions import AggResponse
from polygon_api.definitions import ReferenceTickersApiResponse
from polygon_api.definitions import ReferenceTickersV3ApiResponse
from polygon_api.definitions import ReferenceTickerTypesApiResponse
from polygon_api.definitions import ReferenceTickerDetailsApiResponse
from polygon_api.definitions import ReferenceTickerDetailsV3ApiResponse
from polygon_api.definitions import ReferenceTickerNewsApiResponse
from polygon_api.definitions import ReferenceTickerNewsV2ApiResponse
from polygon_api.definitions import ReferenceMarketsApiResponse
from polygon_api.definitions import ReferenceLocalesApiResponse
from polygon_api.definitions import ReferenceStockSplitsApiResponse
from polygon_api.definitions import ReferenceStockDividendsApiResponse
from polygon_api.definitions import ReferenceStockFinancialsApiResponse
from polygon_api.definitions import ReferenceMarketStatusApiResponse
from polygon_api.definitions import ReferenceMarketHolidaysApiResponse
from polygon_api.definitions import StocksEquitiesExchangesApiResponse
from polygon_api.definitions import StocksEquitiesHistoricTradesApiResponse
from polygon_api.definitions import HistoricTradesV2ApiResponse
from polygon_api.definitions import StocksEquitiesHistoricQuotesApiResponse
from polygon_api.definitions import HistoricNBboQuotesV2ApiResponse
from polygon_api.definitions import StocksEquitiesLastTradeForASymbolApiResponse
from polygon_api.definitions import StocksEquitiesLastQuoteForASymbolApiResponse
from polygon_api.definitions import StocksEquitiesDailyOpenCloseApiResponse
from polygon_api.definitions import StocksEquitiesConditionMappingsApiResponse
from polygon_api.definitions import StocksEquitiesSnapshotAllTickersApiResponse
from polygon_api.definitions import StocksEquitiesSnapshotSingleTickerApiResponse
from polygon_api.definitions import StocksEquitiesSnapshotGainersLosersApiResponse
from polygon_api.definitions import StocksEquitiesPreviousCloseApiResponse
from polygon_api.definitions import StocksEquitiesAggregatesApiResponse
from polygon_api.definitions import StocksEquitiesGroupedDailyApiResponse
from polygon_api.definitions import ForexCurrenciesHistoricForexTicksApiResponse
from polygon_api.definitions import ForexCurrenciesRealTimeCurrencyConversionApiResponse
from polygon_api.definitions import ForexCurrenciesLastQuoteForACurrencyPairApiResponse
from polygon_api.definitions import ForexCurrenciesGroupedDailyApiResponse
from polygon_api.definitions import ForexCurrenciesPreviousCloseApiResponse
from polygon_api.definitions import ForexCurrenciesSnapshotAllTickersApiResponse
from polygon_api.definitions import ForexCurrenciesSnapshotSingleTickerApiResponse
from polygon_api.definitions import ForexCurrenciesSnapshotGainersLosersApiResponse
from polygon_api.definitions import CryptoCryptoExchangesApiResponse
from polygon_api.definitions import CryptoLastTradeForACryptoPairApiResponse
from polygon_api.definitions import CryptoDailyOpenCloseApiResponse
from polygon_api.definitions import CryptoHistoricCryptoTradesApiResponse
from polygon_api.definitions import CryptoGroupedDailyApiResponse
from polygon_api.definitions import CryptoPreviousCloseApiResponse
from polygon_api.definitions import CryptoSnapshotAllTickersApiResponse
from polygon_api.definitions import CryptoSnapshotSingleTickerApiResponse
from polygon_api.definitions import CryptoSnapshotSingleTickerFullBookApiResponse
from polygon_api.definitions import CryptoSnapshotGainersLosersApiResponse
from polygon_api.definitions import CurrenciesAggregatesApiResponse
from polygon_api.definitions import StockSymbol
from polygon_api.definitions import ConditionTypeMap
from polygon_api.definitions import SymbolTypeMap
from polygon_api.definitions import TickerSymbol


import typing
from polygon_api.definitions import Definition


AnyDefinition = typing.TypeVar("AnyDefinition", bound=Definition)

# noinspection SpellCheckingInspection
name_to_class: typing.Dict[str, typing.Callable[[], typing.Type[AnyDefinition]]] = {
    "LastTrade": LastTrade,
    "LastQuote": LastQuote,
    "HistTrade": HistTrade,
    "Quote": Quote,
    "Aggregate": Aggregate,
    "Company": Company,
    "CompanyV3": CompanyV3,
    "Address": Address,
    "Symbol": Symbol,
    "Dividend": Dividend,
    "News": News,
    "NewsV2": NewsV2,
    "Publisher": Publisher,
    "Earning": Earning,
    "Financial": Financial,
    "Exchange": Exchange,
    "Error": Error,
    "NotFound": NotFound,
    "Conflict": Conflict,
    "Unauthorized": Unauthorized,
    "MarketStatus": MarketStatus,
    "MarketHoliday": MarketHoliday,
    "AnalystRatings": AnalystRatings,
    "RatingSection": RatingSection,
    "CryptoTick": CryptoTick,
    "CryptoTickJson": CryptoTickJson,
    "CryptoExchange": CryptoExchange,
    "CryptoSnapshotTicker": CryptoSnapshotTicker,
    "CryptoSnapshotBookItem": CryptoSnapshotBookItem,
    "CryptoSnapshotTickerBook": CryptoSnapshotTickerBook,
    "CryptoSnapshotAgg": CryptoSnapshotAgg,
    "Forex": Forex,
    "LastForexTrade": LastForexTrade,
    "LastForexQuote": LastForexQuote,
    "ForexAggregate": ForexAggregate,
    "ForexSnapshotTicker": ForexSnapshotTicker,
    "ForexSnapshotAgg": ForexSnapshotAgg,
    "Ticker": Ticker,
    "Split": Split,
    "Financials": Financials,
    "Trade": Trade,
    "StocksSnapshotTicker": StocksSnapshotTicker,
    "StocksSnapshotBookItem": StocksSnapshotBookItem,
    "StocksSnapshotTickerBook": StocksSnapshotTickerBook,
    "StocksV2Trade": StocksV2Trade,
    "StocksV2NBBO": StocksV2NBBO,
    "StocksSnapshotAgg": StocksSnapshotAgg,
    "StocksSnapshotQuote": StocksSnapshotQuote,
    "Aggv2": Aggv2,
    "AggResponse": AggResponse,
    "ReferenceTickersApiResponse": ReferenceTickersApiResponse,
    "ReferenceTickersV3ApiResponse": ReferenceTickersV3ApiResponse,
    "ReferenceTickerTypesApiResponse": ReferenceTickerTypesApiResponse,
    "ReferenceTickerDetailsApiResponse": ReferenceTickerDetailsApiResponse,
    "ReferenceTickerDetailsV3ApiResponse": ReferenceTickerDetailsV3ApiResponse,
    "ReferenceTickerNewsApiResponse": ReferenceTickerNewsApiResponse,
    "ReferenceTickerNewsV2ApiResponse": ReferenceTickerNewsV2ApiResponse,
    "ReferenceMarketsApiResponse": ReferenceMarketsApiResponse,
    "ReferenceLocalesApiResponse": ReferenceLocalesApiResponse,
    "ReferenceStockSplitsApiResponse": ReferenceStockSplitsApiResponse,
    "ReferenceStockDividendsApiResponse": ReferenceStockDividendsApiResponse,
    "ReferenceStockFinancialsApiResponse": ReferenceStockFinancialsApiResponse,
    "ReferenceMarketStatusApiResponse": ReferenceMarketStatusApiResponse,
    "ReferenceMarketHolidaysApiResponse": ReferenceMarketHolidaysApiResponse,
    "StocksEquitiesExchangesApiResponse": StocksEquitiesExchangesApiResponse,
    "StocksEquitiesHistoricTradesApiResponse": StocksEquitiesHistoricTradesApiResponse,
    "HistoricTradesV2ApiResponse": HistoricTradesV2ApiResponse,
    "StocksEquitiesHistoricQuotesApiResponse": StocksEquitiesHistoricQuotesApiResponse,
    "HistoricNBboQuotesV2ApiResponse": HistoricNBboQuotesV2ApiResponse,
    "StocksEquitiesLastTradeForASymbolApiResponse": StocksEquitiesLastTradeForASymbolApiResponse,
    "StocksEquitiesLastQuoteForASymbolApiResponse": StocksEquitiesLastQuoteForASymbolApiResponse,
    "StocksEquitiesDailyOpenCloseApiResponse": StocksEquitiesDailyOpenCloseApiResponse,
    "StocksEquitiesConditionMappingsApiResponse": StocksEquitiesConditionMappingsApiResponse,
    "StocksEquitiesSnapshotAllTickersApiResponse": StocksEquitiesSnapshotAllTickersApiResponse,
    "StocksEquitiesSnapshotSingleTickerApiResponse": StocksEquitiesSnapshotSingleTickerApiResponse,
    "StocksEquitiesSnapshotGainersLosersApiResponse": StocksEquitiesSnapshotGainersLosersApiResponse,
    "StocksEquitiesPreviousCloseApiResponse": StocksEquitiesPreviousCloseApiResponse,
    "StocksEquitiesAggregatesApiResponse": StocksEquitiesAggregatesApiResponse,
    "StocksEquitiesGroupedDailyApiResponse": StocksEquitiesGroupedDailyApiResponse,
    "ForexCurrenciesHistoricForexTicksApiResponse": ForexCurrenciesHistoricForexTicksApiResponse,
    "ForexCurrenciesRealTimeCurrencyConversionApiResponse": ForexCurrenciesRealTimeCurrencyConversionApiResponse,
    "ForexCurrenciesLastQuoteForACurrencyPairApiResponse": ForexCurrenciesLastQuoteForACurrencyPairApiResponse,
    "ForexCurrenciesGroupedDailyApiResponse": ForexCurrenciesGroupedDailyApiResponse,
    "ForexCurrenciesPreviousCloseApiResponse": ForexCurrenciesPreviousCloseApiResponse,
    "ForexCurrenciesSnapshotAllTickersApiResponse": ForexCurrenciesSnapshotAllTickersApiResponse,
    "ForexCurrenciesSnapshotSingleTickerApiResponse": ForexCurrenciesSnapshotSingleTickerApiResponse,
    "ForexCurrenciesSnapshotGainersLosersApiResponse": ForexCurrenciesSnapshotGainersLosersApiResponse,
    "CryptoCryptoExchangesApiResponse": CryptoCryptoExchangesApiResponse,
    "CryptoLastTradeForACryptoPairApiResponse": CryptoLastTradeForACryptoPairApiResponse,
    "CryptoDailyOpenCloseApiResponse": CryptoDailyOpenCloseApiResponse,
    "CryptoHistoricCryptoTradesApiResponse": CryptoHistoricCryptoTradesApiResponse,
    "CryptoGroupedDailyApiResponse": CryptoGroupedDailyApiResponse,
    "CryptoPreviousCloseApiResponse": CryptoPreviousCloseApiResponse,
    "CryptoSnapshotAllTickersApiResponse": CryptoSnapshotAllTickersApiResponse,
    "CryptoSnapshotSingleTickerApiResponse": CryptoSnapshotSingleTickerApiResponse,
    "CryptoSnapshotSingleTickerFullBookApiResponse": CryptoSnapshotSingleTickerFullBookApiResponse,
    "CryptoSnapshotGainersLosersApiResponse": CryptoSnapshotGainersLosersApiResponse,
    "CurrenciesAggregatesApiResponse": CurrenciesAggregatesApiResponse,

}

# noinspection SpellCheckingInspection
name_to_type = {
    "StockSymbol": StockSymbol,
    "ConditionTypeMap": ConditionTypeMap,
    "SymbolTypeMap": SymbolTypeMap,
    "TickerSymbol": TickerSymbol,

}