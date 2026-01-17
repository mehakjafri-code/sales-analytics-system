from utils.data_processor import daily_sales_trend
from utils.file_handler import read_sales_file, write_output
from utils.data_processor import clean_and_validate, calculate_total_revenue
from utils.api_handler import get_usd_rate

# Step 1: Read + clean
lines = read_sales_file("data/sales_data.txt")
records = clean_and_validate(lines)

# Step 2: Calculate total revenue (Q3 Part 1a)
total_revenue = calculate_total_revenue(records)

# Step 3: USD conversion
usd_rate = get_usd_rate()
usd_revenue = total_revenue * usd_rate if usd_rate else "API Error"

# Step 4: Build report
report = "SALES REPORT\n\n"
report += f"Total Revenue (INR): {total_revenue}\n"
report += f"Total Revenue (USD): {usd_revenue}\n\n"

write_output("summary.txt", report)

print("Total Revenue:", total_revenue)
print("Final report saved to output/summary.txt")
print(records[0])
daily = daily_sales_trend(records)

print("\nDAILY SALES TREND (sample):")
for date, stats in list(daily.items())[:3]:
    print(date, stats)



