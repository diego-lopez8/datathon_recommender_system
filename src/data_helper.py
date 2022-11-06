import pandas as pd
import glob
import numpy as np
from datetime import datetime
from math import isnan
import os


def create_time_features(orders):
    '''
    This function uses the raw timestamp data for the orders to create two new features:
    month of purchase and time of day of purchase.

    :param orders: pandas DataFrame containing raw orders data
    '''

    if os.path.exists('../data/processed/olist_orders_reduced2.csv'):
        return

    def get_time_of_day(time):
        time = int(time)
        if time >= 5 and time < 12:
            return 'morning'
        elif time >= 12 and time < 16:
            return 'afternoon'
        elif time >= 16 and time < 23:
            return 'evening'
        else:
            return 'night'

    timestamps = orders['order_purchase_timestamp']
    new_features = pd.DataFrame(columns=['purchase_month', 'purchase_time'],
                                index=range(len(timestamps)))

    for i in range(len(timestamps)):
        stamp = timestamps[i].split(' ')[0].split('-')
        new_features.loc[i, 'purchase_month'] = stamp[1]
        new_features.loc[i, 'purchase_time'] = get_time_of_day(stamp[-1])

    orders = orders.join(new_features)
    print(orders)


def create_product_features():
    files = glob.glob('../data/raw/archive/*.csv')
    datasets = {f.split('/')[-1][:-4].replace('olist_', '').replace('_dataset', ''):
                    pd.read_csv(f) for f in files}

    orders = datasets['orders']
    create_time_features(orders)

