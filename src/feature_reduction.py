import pandas as pd

olist_customers = pd.read_csv("../data/raw/archive/olist_customers_dataset.csv")
olist_geolocation = pd.read_csv("../data/raw/archive/olist_geolocation_dataset.csv")
olist_order_items = pd.read_csv("../data/raw/archive/olist_order_items_dataset.csv")
olist_order_payments = pd.read_csv("../data/raw/archive/olist_order_payments_dataset.csv")
olist_order_reviews = pd.read_csv("../data/raw/archive/olist_order_reviews_dataset.csv")
olist_orders = pd.read_csv("../data/raw/archive/olist_orders_dataset.csv")
olist_products = pd.read_csv("../data/raw/archive/olist_products_dataset.csv")
olist_sellers = pd.read_csv("../data/raw/archive/olist_sellers_dataset.csv")
olist_product_name_translation = pd.read_csv("../data/raw/archive/product_category_name_translation.csv")

olist_sellers.drop(columns=["seller_city", "seller_zip_code_prefix"]).to_csv("../data/processed/olist_sellers_reduced.csv")
olist_orders.drop(columns=["order_approved_at"]).to_csv("../data/processed/olist_orders_reduced.csv")
olist_order_items.drop(columns=['shipping_limit_date']).to_csv("../data/processed/olist_orders_items_reduced.csv")
olist_order_payments.drop(columns=["payment_sequential", "payment_value"]).to_csv("../data/processed/olist_order_payments_reduced.csv")
olist_order_reviews.drop(columns=["review_comment_title", "review_comment_message", "review_creation_date","review_answer_timestamp"]).to_csv("../data/processed/olist_order_reviews_reduced.csv")
