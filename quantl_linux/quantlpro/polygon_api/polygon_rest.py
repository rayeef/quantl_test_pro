from typing import Dict, Type
import datetime
import requests
#import library
import polygon_api.library
import polygon_api.unmarshal

library = polygon_api.library
unmarshal = polygon_api.unmarshal

class RESTClient:
    """ This is a custom generated class """
    DEFAULT_HOST = "api.polygon.io"

    def __init__(self, auth_key: str, timeout: int = None):
        self.auth_key = auth_key
        self.url = "https://" + self.DEFAULT_HOST

        self._session = requests.Session()
        self._session.params["apiKey"] = self.auth_key
        self.timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._session.close()

    def ts_to_datetime(ts) -> str:
        return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')

    def _handle_response(self, response_type: str, endpoint: str, params: Dict[str, str]) -> Type[library.AnyDefinition]:
        resp: requests.Response = self._session.get(endpoint, params=params, timeout=self.timeout)
        if resp.status_code == 200:
            return unmarshal.unmarshal_json(response_type, resp.json())
        else:
            resp.raise_for_status()

    def reference_tickers(self, **query_params) -> library.ReferenceTickersApiResponse:
        endpoint = f"{self.url}/v2/reference/tickers"
        return self._handle_response("ReferenceTickersApiResponse", endpoint, query_params)

    def reference_tickers_v3(self, next_url=None, **query_params) -> library.ReferenceTickersV3ApiResponse:
        endpoint = f"{self.url}/v3/reference/tickers" if not next_url else next_url
        return self._handle_response("ReferenceTickersV3ApiResponse", endpoint, query_params)

    def reference_ticker_types(self, **query_params) -> library.ReferenceTickerTypesApiResponse:
        endpoint = f"{self.url}/v2/reference/types"
        return self._handle_response("ReferenceTickerTypesApiResponse", endpoint, query_params)

    def reference_ticker_details(self, symbol, **query_params) -> library.ReferenceTickerDetailsApiResponse:
        endpoint = f"{self.url}/v1/meta/symbols/{symbol}/company"
        return self._handle_response("ReferenceTickerDetailsApiResponse", endpoint, query_params)

    def reference_ticker_details_vx(self, symbol, **query_params) -> library.ReferenceTickerDetailsV3ApiResponse:
        endpoint = f"{self.url}/vX/reference/tickers/{symbol}"
        return self._handle_response("ReferenceTickerDetailsV3ApiResponse", endpoint, query_params)

    def reference_ticker_news(self, symbol, **query_params) -> library.ReferenceTickerNewsApiResponse:
        endpoint = f"{self.url}/v1/meta/symbols/{symbol}/news"
        return self._handle_response("ReferenceTickerNewsApiResponse", endpoint, query_params)

    def reference_ticker_news_v2(self, **query_params) -> library.ReferenceTickerNewsV2ApiResponse:
        endpoint = f"{self.url}/v2/reference/news"
        return self._handle_response("ReferenceTickerNewsV2ApiResponse", endpoint, query_params)

    def reference_markets(self, **query_params) -> library.ReferenceMarketsApiResponse:
        endpoint = f"{self.url}/v2/reference/markets"
        return self._handle_response("ReferenceMarketsApiResponse", endpoint, query_params)

    def reference_locales(self, **query_params) -> library.ReferenceLocalesApiResponse:
        endpoint = f"{self.url}/v2/reference/locales"
        return self._handle_response("ReferenceLocalesApiResponse", endpoint, query_params)

    def reference_stock_splits(self, symbol, **query_params) -> library.ReferenceStockSplitsApiResponse:
        endpoint = f"{self.url}/v2/reference/splits/{symbol}"
        return self._handle_response("ReferenceStockSplitsApiResponse", endpoint, query_params)

    def reference_stock_dividends(self, symbol, **query_params) -> library.ReferenceStockDividendsApiResponse:
        endpoint = f"{self.url}/v2/reference/dividends/{symbol}"
        return self._handle_response("ReferenceStockDividendsApiResponse", endpoint, query_params)

    def reference_stock_financials(self, symbol, **query_params) -> library.ReferenceStockFinancialsApiResponse:
        endpoint = f"{self.url}/v2/reference/financials/{symbol}"
        return self._handle_response("ReferenceStockFinancialsApiResponse", endpoint, query_params)

    def reference_market_status(self, **query_params) -> library.ReferenceMarketStatusApiResponse:
        endpoint = f"{self.url}/v1/marketstatus/now"
        return self._handle_response("ReferenceMarketStatusApiResponse", endpoint, query_params)

    def reference_market_holidays(self, **query_params) -> library.ReferenceMarketHolidaysApiResponse:
        endpoint = f"{self.url}/v1/marketstatus/upcoming"
        return self._handle_response("ReferenceMarketHolidaysApiResponse", endpoint, query_params)

    def stocks_equities_exchanges(self, **query_params) -> library.StocksEquitiesExchangesApiResponse:
        endpoint = f"{self.url}/v1/meta/exchanges"
        return self._handle_response("StocksEquitiesExchangesApiResponse", endpoint, query_params)

    def stocks_equities_historic_trades(self, symbol, date,
                                        **query_params) -> library.StocksEquitiesHistoricTradesApiResponse:
        endpoint = f"{self.url}/v1/historic/trades/{symbol}/{date}"
        return self._handle_response("StocksEquitiesHistoricTradesApiResponse", endpoint, query_params)

    def historic_trades_v2(self, ticker, date, **query_params) -> library.HistoricTradesV2ApiResponse:
        endpoint = f"{self.url}/v2/ticks/stocks/trades/{ticker}/{date}"
        return self._handle_response("HistoricTradesV2ApiResponse", endpoint, query_params)

    def stocks_equities_historic_quotes(self, symbol, date,
                                        **query_params) -> library.StocksEquitiesHistoricQuotesApiResponse:
        endpoint = f"{self.url}/v1/historic/quotes/{symbol}/{date}"
        return self._handle_response("StocksEquitiesHistoricQuotesApiResponse", endpoint, query_params)

    def historic_n___bbo_quotes_v2(self, ticker, date, **query_params) -> library.HistoricNBboQuotesV2ApiResponse:
        endpoint = f"{self.url}/v2/ticks/stocks/nbbo/{ticker}/{date}"
        return self._handle_response("HistoricNBboQuotesV2ApiResponse", endpoint, query_params)

    def stocks_equities_last_trade_for_a_symbol(self, symbol,
                                                **query_params) -> library.StocksEquitiesLastTradeForASymbolApiResponse:
        endpoint = f"{self.url}/v1/last/stocks/{symbol}"
        return self._handle_response("StocksEquitiesLastTradeForASymbolApiResponse", endpoint, query_params)

    def stocks_equities_last_quote_for_a_symbol(self, symbol,
                                                **query_params) -> library.StocksEquitiesLastQuoteForASymbolApiResponse:
        endpoint = f"{self.url}/v1/last_quote/stocks/{symbol}"
        return self._handle_response("StocksEquitiesLastQuoteForASymbolApiResponse", endpoint, query_params)

    def stocks_equities_daily_open_close(self, symbol, date,
                                         **query_params) -> library.StocksEquitiesDailyOpenCloseApiResponse:
        endpoint = f"{self.url}/v1/open-close/{symbol}/{date}"
        return self._handle_response("StocksEquitiesDailyOpenCloseApiResponse", endpoint, query_params)

    def stocks_equities_condition_mappings(self, ticktype,
                                           **query_params) -> library.StocksEquitiesConditionMappingsApiResponse:
        endpoint = f"{self.url}/v1/meta/conditions/{ticktype}"
        return self._handle_response("StocksEquitiesConditionMappingsApiResponse", endpoint, query_params)

    def stocks_equities_snapshot_all_tickers(self,
                                             **query_params) -> library.StocksEquitiesSnapshotAllTickersApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/us/markets/stocks/tickers"
        return self._handle_response("StocksEquitiesSnapshotAllTickersApiResponse", endpoint, query_params)

    def stocks_equities_snapshot_single_ticker(self, ticker,
                                               **query_params) -> library.StocksEquitiesSnapshotSingleTickerApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}"
        return self._handle_response("StocksEquitiesSnapshotSingleTickerApiResponse", endpoint, query_params)

    def stocks_equities_snapshot_gainers_losers(self, direction,
                                                **query_params) -> library.StocksEquitiesSnapshotGainersLosersApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/us/markets/stocks/{direction}"
        return self._handle_response("StocksEquitiesSnapshotGainersLosersApiResponse", endpoint, query_params)

    def stocks_equities_previous_close(self, ticker, **query_params) -> library.StocksEquitiesPreviousCloseApiResponse:
        endpoint = f"{self.url}/v2/aggs/ticker/{ticker}/prev"
        return self._handle_response("StocksEquitiesPreviousCloseApiResponse", endpoint, query_params)

    def stocks_equities_aggregates(self, ticker, multiplier, timespan, from_, to,
                                   **query_params) -> library.StocksEquitiesAggregatesApiResponse:
        endpoint = f"{self.url}/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}"
        return self._handle_response("StocksEquitiesAggregatesApiResponse", endpoint, query_params)

    def stocks_equities_grouped_daily(self, locale, market, date,
                                      **query_params) -> library.StocksEquitiesGroupedDailyApiResponse:
        endpoint = f"{self.url}/v2/aggs/grouped/locale/{locale}/market/{market}/{date}"
        return self._handle_response("StocksEquitiesGroupedDailyApiResponse", endpoint, query_params)

    def forex_currencies_historic_forex_ticks(self, from_, to, date,
                                              **query_params) -> library.ForexCurrenciesHistoricForexTicksApiResponse:
        endpoint = f"{self.url}/v1/historic/forex/{from_}/{to}/{date}"
        return self._handle_response("ForexCurrenciesHistoricForexTicksApiResponse", endpoint, query_params)

    def forex_currencies_real_time_currency_conversion(self, from_, to,
                                                       **query_params) -> library.ForexCurrenciesRealTimeCurrencyConversionApiResponse:
        endpoint = f"{self.url}/v1/conversion/{from_}/{to}"
        return self._handle_response("ForexCurrenciesRealTimeCurrencyConversionApiResponse", endpoint, query_params)

    def forex_currencies_last_quote_for_a_currency_pair(self, from_, to,
                                                        **query_params) -> library.ForexCurrenciesLastQuoteForACurrencyPairApiResponse:
        endpoint = f"{self.url}/v1/last_quote/currencies/{from_}/{to}"
        return self._handle_response("ForexCurrenciesLastQuoteForACurrencyPairApiResponse", endpoint, query_params)

    def forex_currencies_grouped_daily(self, date, **query_params) -> library.ForexCurrenciesGroupedDailyApiResponse:
        endpoint = f"{self.url}/v2/aggs/grouped/locale/global/market/fx/{date}"
        return self._handle_response("ForexCurrenciesGroupedDailyApiResponse", endpoint, query_params)

    def forex_currencies_previous_close(self, ticker, **query_params) -> library.ForexCurrenciesGroupedDailyApiResponse:
        endpoint = f"{self.url}/v2/aggs/ticker/{ticker}/prev"
        return self._handle_response("ForexCurrenciesPreviousCloseApiResponse", endpoint, query_params)

    def forex_currencies_snapshot_all_tickers(self,
                                              **query_params) -> library.ForexCurrenciesSnapshotAllTickersApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/forex/tickers"
        return self._handle_response("ForexCurrenciesSnapshotAllTickersApiResponse", endpoint, query_params)

    def forex_currencies_snapshot_single_ticker(self, ticker,
                                                **query_params) -> library.ForexCurrenciesSnapshotSingleTickerApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/forex/tickers/{ticker}"
        return self._handle_response("ForexCurrenciesSnapshotSingleTickerApiResponse", endpoint, query_params)

    def forex_currencies_snapshot_gainers_losers(self, direction,
                                                 **query_params) -> library.ForexCurrenciesSnapshotGainersLosersApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/forex/{direction}"
        return self._handle_response("ForexCurrenciesSnapshotGainersLosersApiResponse", endpoint, query_params)

    def forex_currencies_aggregates(self, ticker, multiplier, timespan, from_, to,
                                    **query_params) -> library.CurrenciesAggregatesApiResponse:
        endpoint = f"{self.url}/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}"
        return self._handle_response("CurrenciesAggregatesApiResponse", endpoint, query_params)

    def crypto_crypto_exchanges(self, **query_params) -> library.CryptoCryptoExchangesApiResponse:
        endpoint = f"{self.url}/v1/meta/crypto-exchanges"
        return self._handle_response("CryptoCryptoExchangesApiResponse", endpoint, query_params)

    def crypto_last_trade_for_a_crypto_pair(self, from_, to,
                                            **query_params) -> library.CryptoLastTradeForACryptoPairApiResponse:
        endpoint = f"{self.url}/v1/last/crypto/{from_}/{to}"
        return self._handle_response("CryptoLastTradeForACryptoPairApiResponse", endpoint, query_params)

    def crypto_daily_open_close(self, from_, to, date, **query_params) -> library.CryptoDailyOpenCloseApiResponse:
        endpoint = f"{self.url}/v1/open-close/crypto/{from_}/{to}/{date}"
        return self._handle_response("CryptoDailyOpenCloseApiResponse", endpoint, query_params)

    def crypto_aggregates(self, ticker, multiplier, timespan, from_, to,
                          **query_params) -> library.CurrenciesAggregatesApiResponse:
        endpoint = f"{self.url}/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}"
        return self._handle_response("CurrenciesAggregatesApiResponse", endpoint, query_params)

    def crypto_historic_crypto_trades(self, from_, to, date,
                                      **query_params) -> library.CryptoHistoricCryptoTradesApiResponse:
        endpoint = f"{self.url}/v1/historic/crypto/{from_}/{to}/{date}"
        return self._handle_response("CryptoHistoricCryptoTradesApiResponse", endpoint, query_params)

    def crypto_grouped_daily(self, date, **query_params) -> library.CryptoGroupedDailyApiResponse:
        endpoint = f"{self.url}/v2/aggs/grouped/locale/global/market/crypto/{date}"
        return self._handle_response("CryptoGroupedDailyApiResponse", endpoint, query_params)

    def crypto_previous_close(self, ticker, **query_params) -> library.CryptoPreviousCloseApiResponse:
        endpoint = f"{self.url}/v2/aggs/ticker/{ticker}/prev"
        return self._handle_response("CryptoPreviousCloseApiResponse", endpoint, query_params)

    def crypto_snapshot_all_tickers(self, **query_params) -> library.CryptoSnapshotAllTickersApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/crypto/tickers"
        return self._handle_response("CryptoSnapshotAllTickersApiResponse", endpoint, query_params)

    def crypto_snapshot_single_ticker(self, ticker, **query_params) -> library.CryptoSnapshotSingleTickerApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}"
        return self._handle_response("CryptoSnapshotSingleTickerApiResponse", endpoint, query_params)

    def crypto_snapshot_single_ticker_full_book(self, ticker,
                                                **query_params) -> library.CryptoSnapshotSingleTickerFullBookApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}/book"
        return self._handle_response("CryptoSnapshotSingleTickerFullBookApiResponse", endpoint, query_params)

    def crypto_snapshot_gainers_losers(self, direction,
                                       **query_params) -> library.CryptoSnapshotGainersLosersApiResponse:
        endpoint = f"{self.url}/v2/snapshot/locale/global/markets/crypto/{direction}"
        return self._handle_response("CryptoSnapshotGainersLosersApiResponse", endpoint, query_params)

