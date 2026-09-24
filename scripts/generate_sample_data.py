import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_synthetic_cloudmart_dataset(output_dir: str = "data/sample", dashboard_dir: str = "dashboard"):
    """Generates synthetic e-commerce sales datasets for testing and Streamlit dashboard snapshots."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(dashboard_dir, exist_ok=True)
    np.random.seed(42)
    random.seed(42)

    num_customers = 500
    num_products = 50
    num_orders = 5000

    # 1. Customers Dimension Data
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    segments = ["Standard", "Premium", "VIP"]
    countries = ["United States", "Canada", "United Kingdom", "Germany", "Japan", "Australia"]

    customers = []
    for i in range(1, num_customers + 1):
        cust_id = f"CUST_{i:04d}"
        customers.append({
            "customer_key": i,
            "customer_id": cust_id,
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "email": f"cust_{i}@example.com",
            "customer_segment": random.choices(segments, weights=[0.6, 0.3, 0.1])[0],
            "country": random.choice(countries),
            "city": "Sample City",
            "postal_code": f"{random.randint(10000, 99999)}",
            "effective_date": "2025-01-01",
            "end_date": "9999-12-31",
            "is_current": True,
            "version": 1
        })
    df_customers = pd.DataFrame(customers)

    # 2. Products Dimension Data
    categories = {
        "Consumer Electronics": ["Smartphones", "Laptops", "Audio Headphones", "Smartwatches"],
        "Home & Kitchen": ["Coffee Makers", "Air Fryers", "Blenders", "Robotic Vacuums"],
        "Apparel & Fashion": ["Men's Jackets", "Women's Sneakers", "Sportswear", "Watches"],
        "Books & Media": ["Hardcover Novels", "Tech Guides", "Audiobooks"]
    }

    products = []
    prod_id_counter = 1
    for cat, subcats in categories.items():
        for subcat in subcats:
            for item_idx in range(1, 4):
                cost = round(random.uniform(15.0, 300.0), 2)
                price = round(cost * random.uniform(1.3, 2.2), 2)
                products.append({
                    "product_key": prod_id_counter,
                    "product_id": f"PROD_{prod_id_counter:04d}",
                    "product_name": f"{subcat} Pro-Series {item_idx}",
                    "category": cat,
                    "subcategory": subcat,
                    "brand": "CloudMart Elite",
                    "unit_cost": cost,
                    "list_price": price,
                    "effective_date": "2025-01-01",
                    "end_date": "9999-12-31",
                    "is_current": True,
                    "version": 1
                })
                prod_id_counter += 1
    df_products = pd.DataFrame(products)

    # 3. Regions Dimension Data
    regions = [
        {"region_key": 1, "region_id": "REG_01", "region_name": "North America", "country_code": "US", "manager_name": "Sarah Connor"},
        {"region_key": 2, "region_id": "REG_02", "region_name": "EMEA", "country_code": "DE", "manager_name": "Hans Gruber"},
        {"region_key": 3, "region_id": "REG_03", "region_name": "APAC", "country_code": "JP", "manager_name": "Kenji Sato"},
        {"region_key": 4, "region_id": "REG_04", "region_name": "LATAM", "country_code": "BR", "manager_name": "Carlos Silva"}
    ]
    df_regions = pd.DataFrame(regions)

    # 4. Fact Sales Transactions Data
    from datetime import timezone
    start_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    orders = []

    for i in range(1, num_orders + 1):
        order_date = start_date + timedelta(days=random.randint(0, 600), hours=random.randint(0, 23))
        cust = random.choice(customers)
        prod = random.choice(products)
        reg = random.choice(regions)

        qty = random.randint(1, 5)
        unit_price = prod["list_price"]
        discount = round(unit_price * qty * random.choice([0.0, 0.05, 0.10, 0.15]), 2)
        gross = round(qty * unit_price, 2)
        net = round(gross - discount, 2)

        date_key = int(order_date.strftime("%Y%m%d"))

        orders.append({
            "sales_fact_id": i,
            "order_id": f"ORD_{100000 + i}",
            "order_line_number": 1,
            "customer_key": cust["customer_key"],
            "customer_id": cust["customer_id"],
            "product_key": prod["product_key"],
            "product_id": prod["product_id"],
            "product_name": prod["product_name"],
            "category": prod["category"],
            "date_key": date_key,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "order_timestamp": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "region_key": reg["region_key"],
            "region_name": reg["region_name"],
            "customer_segment": cust["customer_segment"],
            "quantity": qty,
            "unit_price": unit_price,
            "discount_amount": discount,
            "gross_amount": gross,
            "net_amount": net,
            "payment_method": random.choice(["Credit Card", "PayPal", "Apple Pay", "Debit Card"])
        })

    df_sales = pd.DataFrame(orders)

    # Save to sample raw data directory
    df_customers.to_csv(os.path.join(output_dir, "raw_customers.csv"), index=False)
    df_products.to_csv(os.path.join(output_dir, "raw_products.csv"), index=False)
    df_sales.to_csv(os.path.join(output_dir, "raw_orders.csv"), index=False)
    df_regions.to_csv(os.path.join(output_dir, "raw_regions.csv"), index=False)

    # Export combined snapshot for Streamlit dashboard
    df_sales.to_parquet(os.path.join(dashboard_dir, "exported_snapshot.parquet"), index=False)
    df_sales.to_csv(os.path.join(dashboard_dir, "exported_snapshot.csv"), index=False)

    print(f"[SUCCESS] Generated {num_orders} synthetic sales records across {num_customers} customers and {num_products} products.")
    print(f"  - Raw sample files saved in '{output_dir}/'")
    print(f"  - Static dashboard snapshot saved in '{dashboard_dir}/exported_snapshot.parquet'")


if __name__ == "__main__":
    generate_synthetic_cloudmart_dataset()
