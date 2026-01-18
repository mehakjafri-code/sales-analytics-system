from utils.file_handler import read_sales_file
from utils.data_processor import (
    clean_and_validate,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    enrich_sales_data,
    generate_sales_report
)
from utils.api_handler import (
    get_usd_rate,
    fetch_all_products,
    create_product_mapping
)


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1] Read data
        print("\n[1/10] Reading sales data...")
        lines = read_sales_file("data/sales_data.txt")
        print(f"✓ Successfully read {len(lines) - 1} transactions")

        # [2] Parse & clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = clean_and_validate(lines)
        print(f"✓ Parsed {len(transactions)} valid records")

        # [3] Filter options
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(t["region"] for t in transactions))
        amounts = [t["qty"] * t["price"] for t in transactions]

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        if choice == "y":
            region_filter = input("Enter region (or press Enter to skip): ").strip()
            min_amt = input("Min amount (or press Enter to skip): ").strip()
            max_amt = input("Max amount (or press Enter to skip): ").strip()

            filtered = []
            for t in transactions:
                amount = t["qty"] * t["price"]
                if region_filter and t["region"] != region_filter:
                    continue
                if min_amt and amount < float(min_amt):
                    continue
                if max_amt and amount > float(max_amt):
                    continue
                filtered.append(t)

            transactions = filtered
            print(f"✓ Records after filtering: {len(transactions)}")

        # [4] Validation summary
        print("\n[4/10] Validating transactions...")
        print(f"✓ Valid transactions: {len(transactions)}")

        # [5] Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(transactions)
        region_wise_sales(transactions)
        top_selling_products(transactions)
        customer_analysis(transactions)
        daily_sales_trend(transactions)
        find_peak_sales_day(transactions)
        low_performing_products(transactions)
        print("✓ Analysis complete")

        # [6] API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7] Enrichment
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched = enrich_sales_data(transactions, product_mapping)
        success = sum(1 for t in enriched if t["API_Match"])
        print(f"✓ Enriched {success}/{len(enriched)} transactions")

        # [8] Save enriched data
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9] Report
        print("\n[9/10] Generating report...")
        generate_sales_report(transactions, enriched)
        print("✓ Report saved to: output/sales_report.txt")

        # [10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print("Details:", str(e))
        print("Please check your input or data files.")


if __name__ == "__main__":
    main()
