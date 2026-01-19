from utils.file_handler import read_sales_data, write_report
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_purchase_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from datetime import datetime


def main():
    print("=" * 45)
    print("        SALES ANALYTICS SYSTEM")
    print("=" * 45)

    # [1/10] Read data
    print("\n[1/10] Reading sales data...")
    raw_lines = read_sales_data("data/sales_data.txt")
    print(f"✓ Successfully read {len(raw_lines)} transactions")

    # [2/10] Parse & clean
    print("\n[2/10] Parsing and cleaning data...")
    parsed = parse_transactions(raw_lines)
    print(f"✓ Parsed {len(parsed)} records")

    # Show filter options
    regions = sorted(set(t['Region'] for t in parsed))
    amounts = [t['Quantity'] * t['UnitPrice'] for t in parsed]

    print("\n[3/10] Filter Options Available:")
    print("Regions:", ", ".join(regions))
    print(f"Amount Range: Rs.{int(min(amounts)):,} - Rs.{int(max(amounts)):,}")

    apply_filter = input("Do you want to filter data? (y/n): ").lower()

    region = min_amt = max_amt = None
    if apply_filter == 'y':
        region = input("Enter region (or press Enter to skip): ").strip() or None
        min_amt = input("Enter minimum amount (or press Enter): ").strip()
        max_amt = input("Enter maximum amount (or press Enter): ").strip()

        min_amt = float(min_amt) if min_amt else None
        max_amt = float(max_amt) if max_amt else None

    # [4/10] Validation
    print("\n[4/10] Validating transactions...")
    valid, invalid, summary = validate_and_filter(
        parsed, region=region, min_amount=min_amt, max_amount=max_amt
    )
    print(f"✓ Valid: {len(valid)} | Invalid: {invalid}")

    # [5/10] Analysis
    print("\n[5/10] Analyzing sales data...")
    total_revenue = calculate_total_revenue(valid)
    peak_day = find_peak_sales_day(valid)
    low_products = low_performing_products(valid)
    print("✓ Analysis complete")

    # [6/10] API fetch
    print("\n[6/10] Fetching product data from API...")
    api_products = fetch_all_products()
    print(f"✓ Fetched {len(api_products)} products")

    # [7/10] Enrichment
    print("\n[7/10] Enriching sales data...")
    product_mapping = create_product_mapping(api_products)
    enriched = enrich_sales_data(valid, product_mapping)

    enriched_count = sum(1 for t in enriched if t.get("API_Match"))
    rate = (enriched_count / len(enriched)) * 100 if enriched else 0
    print(f"✓ Enriched {enriched_count}/{len(enriched)} transactions ({rate:.1f}%)")

    # [8/10] Save enriched
    print("\n[8/10] Saving enriched data...")
    print("✓ Saved to: data/enriched_sales_data.txt")

    # [9/10] Report generation
    print("\n[9/10] Generating report...")

    avg_order_value = (total_revenue / len(valid)) if valid else 0

    low_products_text = "\n".join(
        f"- {p[0]} | Qty: {p[1]} | Revenue: Rs.{p[2]:,.2f}"
        for p in low_products
    ) if low_products else "None"

    report = (
        "============================================\n"
        "           SALES ANALYTICS REPORT\n"
        f"Generated: {datetime.now()}\n"
        f"Records Processed: {len(valid)}\n"
        "============================================\n\n"

        "OVERALL SUMMARY\n"
        "--------------------------------------------\n"
        f"Total Revenue: Rs.{total_revenue:,.2f}\n"
        f"Total Transactions: {len(valid)}\n"
        f"Average Order Value: Rs.{avg_order_value:,.2f}\n\n"

        "PEAK SALES DAY\n"
        "--------------------------------------------\n"
        f"Date: {peak_day[0]}\n"
        f"Revenue: Rs.{peak_day[1]:,.2f}\n"
        f"Transactions: {peak_day[2]}\n\n"

        "LOW PERFORMING PRODUCTS\n"
        "--------------------------------------------\n"
        f"{low_products_text}\n\n"

        "API ENRICHMENT SUMMARY\n"
        "--------------------------------------------\n"
        f"Enriched Records: {enriched_count}\n"
        f"Success Rate: {rate:.2f}%\n"
    )

    write_report("output/sales_report.txt", report)
    print("✓ Report saved to: output/sales_report.txt")

    # [10/10] Done
    print("\n[10/10] Process Complete!")


if __name__ == "__main__":
    main()
