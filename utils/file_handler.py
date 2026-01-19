def read_sales_data(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()
