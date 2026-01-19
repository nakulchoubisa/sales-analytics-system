import os


def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File not found -> {filename}")
            return []
    else:
        print("Error: Unable to read file due to encoding issues")
        return []

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("TransactionID"):
            continue

        cleaned_lines.append(line)

    return cleaned_lines

def write_report(path, content):
    """
    Writes text report to file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
