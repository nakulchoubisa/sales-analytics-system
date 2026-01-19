import os

def read_sales_data(file_path):
    with open(file_path, "r", encoding="latin-1") as f:
        return f.readlines()

def write_report(path, report):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        for k, v in report.items():
            f.write(f"{k}: {v}\n")
