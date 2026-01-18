from utils.file_handler import read_sales_file, write_output
from utils.data_processor import (
    clean_and_validate,
    calculate_total_revenue,
    enrich_sales_data,
    generate_sales_report
)
from utils.api_handler import (
    get_usd_rate,
    fetch_all_products,
    create_product_mapping
)

# Step 1: Read & clean
lines = read_sales_file("data/sales_data.txt")
records = clean_and_validate(lines)

# Step 2: Revenue
total_revenue = calculate_total_revenue(records)
usd_rate = get_usd_rate()
usd_revenue = total_revenue * usd_rate if usd_rate else "API Error"

# Step 3: Save summary
report = "SALES REPORT\n\n"
report += f"Total Revenue (INR): {total_revenue}\n"
report += f"Total Revenue (USD): {usd_revenue}\n\n"
write_output("summary.txt", report)

# Step 4: API enrichment
api_products = fetch_all_products()
product_mapping = create_product_mapping(api_products)
enriched = enrich_sales_data(records, product_mapping)

# Step 5: Final report
generate_sales_report(records, enriched)

print("✅ Summary saved to output/summary.txt")
print("✅ Enriched data saved to data/enriched_sales_data.txt")
print("✅ Sales report saved to output/sales_report.txt")
