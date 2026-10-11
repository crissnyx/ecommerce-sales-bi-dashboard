import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
n_rows = 1000

dates = [datetime(2026, 1, 1) + timedelta(days=int(np.random.randint(0, 280))) for _ in range(n_rows)]
categories = ['Laptops & Computers', 'Smartphones & Tablets', 'Audio & Sound', 'Gaming & Consoles', 'Smart Home']
products_dict = {
    'Laptops & Computers': ['MacBook Pro M3', 'Lenovo Legion 5', 'ASUS ROG Strix', 'HP Pavilion 15', 'Dell XPS 13'],
    'Smartphones & Tablets': ['iPhone 15 Pro', 'Samsung Galaxy S24', 'iPad Air 5', 'Xiaomi Redmi Note 13', 'Google Pixel 8'],
    'Audio & Sound': ['Sony WH-1000XM4', 'AirPods Pro 2', 'JBL Charge 5', 'Bose QuietComfort', 'Marshall Major IV'],
    'Gaming & Consoles': ['PlayStation 5 Console', 'Xbox Series X', 'Nintendo Switch OLED', 'DualSense Controller', 'Razer DeathAdder V3'],
    'Smart Home': ['Amazon Echo Dot 5', 'Google Nest Hub', 'Philips Hue Bulb Kit', 'Ring Video Doorbell', 'Xiaomi Smart Air Purifier']
}

selected_categories = np.random.choice(categories, n_rows)
selected_products = [np.random.choice(products_dict[cat]) for cat in selected_categories]

base_prices = {
    'MacBook Pro M3': 1899.0, 'Lenovo Legion 5': 1299.0, 'ASUS ROG Strix': 1499.0, 'HP Pavilion 15': 699.0, 'Dell XPS 13': 1199.0,
    'iPhone 15 Pro': 999.0, 'Samsung Galaxy S24': 899.0, 'iPad Air 5': 599.0, 'Xiaomi Redmi Note 13': 299.0, 'Google Pixel 8': 699.0,
    'Sony WH-1000XM4': 278.0, 'AirPods Pro 2': 249.0, 'JBL Charge 5': 149.0, 'Bose QuietComfort': 329.0, 'Marshall Major IV': 149.0,
    'PlayStation 5 Console': 499.0, 'Xbox Series X': 499.0, 'Nintendo Switch OLED': 349.0, 'DualSense Controller': 69.0, 'Razer DeathAdder V3': 69.0,
    'Amazon Echo Dot 5': 49.0, 'Google Nest Hub': 99.0, 'Philips Hue Bulb Kit': 79.0, 'Ring Video Doorbell': 99.0, 'Xiaomi Smart Air Purifier': 159.0
}

prices = [base_prices[p] * np.random.uniform(0.9, 1.1) for p in selected_products]
quantities = np.random.choice([1, 2, 3, 4], n_rows, p=[0.6, 0.25, 0.1, 0.05])
regions = np.random.choice(['North America', 'South America', 'Europe', 'Asia-Pacific'], n_rows, p=[0.4, 0.2, 0.3, 0.1])
channels = np.random.choice(['Direct Web', 'Amazon Marketplace', 'Social Media', 'Affiliates'], n_rows)

df = pd.DataFrame({
    'date': sorted(dates),
    'category': selected_categories,
    'product': selected_products,
    'unit_price': [round(p, 2) for p in prices],
    'quantity': quantities,
    'revenue': [round(p * q, 2) for p, q in zip(prices, quantities)],
    'region': regions,
    'sales_channel': channels
})

df.to_csv('ecommerce_sales_data.csv', index=False)
print("Database 'ecommerce_sales_data.csv' generated successfully!")