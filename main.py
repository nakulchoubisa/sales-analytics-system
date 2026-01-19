from utils.file_handler import read_sales_data, write_report
from utils.data_processor import clean_and_validate, analyze_sales

def main():
    records = read_sales_data("data/sales_data.txt")

    valid_records, stats = clean_and_validate(records)

    # Print validation summary
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Analyze valid records
    report = analyze_sales(valid_records)

    # Write report to output file
    write_report("output/sales_report.txt", report)

if __name__ == "__main__":
    main()

