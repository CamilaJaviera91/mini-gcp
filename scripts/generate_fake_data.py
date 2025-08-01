import csv
import random
import os
from faker import Faker

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)

def get_next_file_number(directory, prefix):
    existing = [f for f in os.listdir(directory) if f.startswith(prefix)]
    numbers = [int(f.replace(prefix, "").replace(".csv", "")) for f in existing if f.replace(prefix, "").replace(".csv", "").isdigit()]
    return max(numbers) + 1 if numbers else 1

output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)
file_number = get_next_file_number(output_dir, "raw_sales_")
output_file = f"{output_dir}/raw_sales_{file_number}.csv"

products = ["Smartphone", "Laptop", "Headphones", "Keyboard", "Monitor",
            "Tablet", "Speaker", "Camera", "Printer", "Mouse"]

with open(output_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "customer", "product", "price", "sale_date"])
    for i in range(1, 5001):
        customer = fake.name()
        product = random.choice(products)
        price = round(random.uniform(10.00, 1000.00), 2)
        sale_date = fake.date_between(start_date="-2y", end_date="today")

        if random.random() < 0.05:
            error_type = random.choice(["missing_customer", "invalid_price", "missing_date", "invalid_product"])
            if error_type == "missing_customer":
                customer = ""
            elif error_type == "invalid_price":
                price = "not_a_price"
            elif error_type == "missing_date":
                sale_date = ""
            elif error_type == "invalid_product":
                product = "UNKNOWN_PRODUCT"

        writer.writerow([i, customer, product, price, sale_date])

print(f"⚠️ Generated {output_file}")
