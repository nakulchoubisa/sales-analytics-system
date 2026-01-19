from utils.file_handler import read_sales_data
from utils.data_processor import process_sales_data

def main():
    data = read_sales_data('data/sales_data.txt')
    result = process_sales_data(data)
    print(result)

if __name__ == "__main__":
    main()
