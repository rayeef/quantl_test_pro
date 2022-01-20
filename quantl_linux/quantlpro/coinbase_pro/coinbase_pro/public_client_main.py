
import cbpro
from public_client import PublicClient
if __name__ == "__main__":

    public_client = PublicClient()

    '''Order Book '''
    order_book = public_client.get_product_order_book('BTC-USD', level=1)
    print('Order Book: ',order_book)
    # Get the product ticker for a specific product.
    public_client.get_product_ticker(product_id='ETH-USD')

    # Get the product trades for a specific product.
    # Returns a generator
    public_client.get_product_trades(product_id='ETH-USD')
    '''Historic Rates'''
    historic_rates =public_client.get_product_historic_rates('ETH-USD')
    print(historic_rates)
    # To include other parameters, see function docstring:
    public_client.get_product_historic_rates('ETH-USD', granularity=300)

    public_client.get_product_24hr_stats('ETH-USD')

    public_client.get_currencies()
