from utils.file_handler import read_sales_file, write_output
from utils.data_processor import clean_and_validate
from utils.api_handler import get_usd_rate

lines = read_sales_file("data/sales_data.txt")
records = clean_and_validate(lines)

total_revenue = 0
region_sales = {}
product_sales = {}

for r in records:
    revenue = r["qty"] * r["price"]
    total_revenue += revenue

    region_sales[r["region"]] = region_sales.get(r["region"], 0) + revenue
    product_sales[r["product"]] = product_sales.get(r["product"], 0) + revenue

best_product = max(product_sales, key=product_sales.get)

usd_rate = get_usd_rate()
usd_revenue = total_revenue * usd_rate if usd_rate else "API Error"

report = "SALES REPORT\n\n"
report += f"Total Revenue (INR): {total_revenue}\n"
report += f"Total Revenue (USD): {usd_revenue}\n\n"

report += "Revenue by Region:\n"
for k, v in region_sales.items():
    report += f"{k}: {v}\n"

report += "\nBest Selling Product:\n"
report += f"{best_product} ({product_sales[best_product]})\n"

write_output("summary.txt", report)
print("\nFinal report saved to output/summary.txt")
