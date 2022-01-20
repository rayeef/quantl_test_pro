
'''Main module that loads the data
    for testing analysis only
'''
import warnings
warnings.filterwarnings('ignore')
from data_loader import *


if __name__ == '__main__':
    i = ['MSFT', 'AMD', 'AAPL', 'V', 'BA']
    for line in i:
        alpha = LoadData(line)
    print(alpha.alpha002(), line)
