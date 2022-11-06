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

    if os.path.exists('../data/processed/olist_orders_reduced.csv'):
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
                                index=range(len(timestamps)), dtype=object)

    for i in range(len(timestamps)):
        stamp = timestamps[i].split(' ')[0].split('-')
        new_features.loc[i, 'purchase_month'] = stamp[1]
        new_features.loc[i, 'purchase_time'] = get_time_of_day(stamp[-1])

    orders = orders.join(new_features)
    orders.to_csv('../data/processed/olist_orders_reduced.csv', index=False)


def create_product_features():
    '''
    This function creates the product features file.
    '''

    if os.path.exists('../data/processed/product_features.csv'):
        return

    files = glob.glob('../data/raw/archive/*.csv')
    datasets = {f.split('/')[-1][:-4].replace('olist_', '').replace('_dataset', ''):
                    pd.read_csv(f) for f in files}

    orders = datasets['orders']
    create_time_features(orders)

    orders = pd.read_csv('../data/processed/olist_orders_reduced.csv', index_col=0)
    order_items = datasets['order_items']
    products = datasets['products']
    customers = pd.read_csv('../data/processed/customer_features.csv', index_col=0)
    reviews = datasets['order_reviews']
    orders = orders.loc[:, ~orders.columns.str.match("Unnamed")]

    orders_products = pd.merge(orders, order_items, left_on=['order_id'],
                               right_on=['order_id'], how='inner')
    orders_products = pd.merge(orders_products, products, left_on=['product_id'],
                               right_on=['product_id'], how='inner')
    products_reviews = pd.merge(orders_products, reviews, left_on=['order_id'],
                                right_on=['order_id'], how='inner')
    orders_times = pd.merge(order_items, datasets['orders'], left_on=['order_id'],
                            right_on=['order_id'], how='inner')

    # Initialize product feature dataframe
    columns = ['product_id', 'product_category_name', 'product_name_lenght', 'product_description_lenght',
               'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm',
               'num_sellers', 'month_most_purchased', 'time_most_purchased', 'num_reviews', 'avg_rating',
               'var_rating', 'avg_delivery_time_days', 'avg_price']

    products = orders_products['product_id'].unique()
    product_features = pd.DataFrame(columns=columns, index=range(len(products)))
    product_features['product_id'] = products

    sellers = {}

    for i in range(len(products)):
        product = products[i]

        product_df = orders_products[orders_products['product_id'] == product]
        review_df = products_reviews[products_reviews['product_id'] == product]
        order_df = orders_times[orders_times['product_id'] == product]

        sellers[product] = list(product_df['seller_id'])
        num_sellers = len(set(sellers[product]))

        months = list(product_df['purchase_month'])
        times = list(product_df['purchase_time'])
        month_most_purchased = max(set(months), key=months.count)
        time_most_purchased = max(set(times), key=times.count)

        num_reviews = review_df['review_id'].nunique()
        scores = list(review_df['review_score'])
        avg_rating = round(np.mean(scores), 1)
        var_rating = round(np.var(scores), 1)

        order_purchase = order_df['order_purchase_timestamp'].dropna()
        order_delivered = order_df['order_delivered_customer_date']

        avg_time = 0
        num_times = 0

        for index, item in order_purchase.items():
            if not isinstance(order_delivered.at[index], str) and isnan(order_delivered.at[index]):
                continue
            d1 = datetime.strptime(item.split(' ')[0], "%Y-%m-%d")
            d2 = datetime.strptime(order_delivered.at[index].split(' ')[0], "%Y-%m-%d")
            avg_time += abs((d2 - d1).days)
            num_times += 1

        if num_times != 0:
            avg_delivery_time_days = int(avg_time / num_times)
        else:
            avg_delivery_time_days = 0

        avg_price = round(np.mean(product_df['price'].tolist()), 2)

        # Set features
        for col in columns[:9]:
            product_features.loc[i, col] = list(set(product_df[col]))[0]

        product_features.loc[i, 'num_sellers'] = num_sellers
        product_features.loc[i, 'month_most_purchased'] = month_most_purchased
        product_features.loc[i, 'time_most_purchased'] = time_most_purchased
        product_features.loc[i, 'num_reviews'] = num_reviews
        product_features.loc[i, 'avg_rating'] = avg_rating
        product_features.loc[i, 'var_rating'] = var_rating
        product_features.loc[i, 'avg_delivery_time_days'] = avg_delivery_time_days
        product_features.loc[i, 'avg_price'] = avg_price

    product_features.to_csv('../data/processed/product_features.csv', index=False)


def create_customer_features():
    '''
    This function creates the customer features file.
    '''

    if os.path.exists('../data/processed/customer_features.csv'):
        return

    files = glob.glob('../data/raw/archive/*.csv')
    datasets = {f.split('/')[-1][:-4].replace('olist_', '').replace('_dataset', ''):
                    pd.read_csv(f) for f in files}

    customers_orders = pd.merge(datasets['orders'], datasets['customers'],
                                left_on=['customer_id'], right_on=['customer_id'], how='inner')
    customers_orders.sort_values(['customer_unique_id'])
    customers = customers_orders['customer_unique_id'].unique()

    num_orders = {}
    for customer in customers:
        orders = customers_orders.loc[customers_orders['customer_unique_id'] == customer]
        if orders.shape[0] not in num_orders:
            num_orders[orders.shape[0]] = orders.shape[0]
        else:
            num_orders[orders.shape[0]] += orders.shape[0]

    columns = ['customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state',
               'number_orders']

    customer_df = pd.DataFrame(columns=columns, index=range(len(customers)))
    customer_df['customer_unique_id'] = customers

    for index, row in customer_df.iterrows():
        customer = row['customer_unique_id']
        df = customers_orders.loc[customers_orders['customer_unique_id'] == customer]
        if df.empty:
            continue

        row['number_orders'] = df['order_id'].nunique()
        row['customer_city'] = df['customer_city'].iloc[0]
        row['customer_state'] = df['customer_state'].iloc[0]
        row['customer_zip_code_prefix'] = df['customer_zip_code_prefix'].iloc[0]

        customer_df.iloc[index] = row

    customer_df.to_csv('../data/processed/customer_features.csv', index=False)
