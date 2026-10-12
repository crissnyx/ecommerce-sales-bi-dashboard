import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Semilla para reproducibilidad
np.random.seed(42)
n_rows = 5000

# Fechas para un rango amplio (2025 - 2026)
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=int(np.random.randint(0, 600))) for _ in range(n_rows)]

regions = ['North America', 'Europe', 'Asia-Pacific', 'South America']
categories = ['Gaming & Consoles', 'Smartphones', 'Laptops & Hardware', 'Audio & Accessories', 'Smart Home']
channels = ['Online Store', 'Mobile App', 'Direct Sales', 'Partner Marketplace']

data = {
    'Date': sorted(dates),
    'Region': np.random.choice(regions, n_rows, p=[0.38, 0.28, 0.22, 0.12]),
    'Category': np.random.choice(categories, n_rows),
    'Sales Channel': np.random.choice(channels, n_rows),
    'Units Sold': np.random.randint(1, 8, n_rows),
    'Total Sales': np.random.uniform(45.0, 1800.0, n_rows).round(2),
    'Cost': np.random.uniform(30.0, 1200.0, n_rows).round(2)
}

df = pd.DataFrame(data)
df.to_csv('ecommerce_sales_data.csv', index=False)
print("¡Dataset masivo generado y guardado exitosamente como 'ecommerce_sales_data.csv'!")