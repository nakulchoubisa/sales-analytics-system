\# Sales Analytics System



This project is a Python-based Sales Data Analytics System built for an e-commerce use case.

It reads messy sales transaction data, cleans and validates records, analyzes sales patterns,

and generates business-ready reports.



---



\## 📂 Project Structure



sales-analytics-system/

├── README.md

├── main.py

├── utils/

│ ├── file\_handler.py

│ ├── data\_processor.py

│ └── api\_handler.py

├── data/

│ └── sales\_data.txt

├── output/

│ └── sales\_report.txt

└── requirements.txt





---



\## ⚙️ Features Implemented



\- Reads pipe-delimited (`|`) sales data

\- Handles non-UTF8 encoding (`latin-1`)

\- Cleans messy product names and numeric values

\- Removes invalid records based on business rules

\- Prints validation summary

\- Generates sales revenue report



---



\## 🧹 Data Cleaning Rules



\### ❌ Records Removed (Invalid)

\- Missing CustomerID or Region

\- Quantity ≤ 0

\- UnitPrice ≤ 0

\- TransactionID not starting with `T`

\- Incorrect number of fields



\### ✅ Records Cleaned \& Kept

\- Commas removed from ProductName

\- Commas removed from numeric values (e.g. `1,500 → 1500`)

\- Empty lines skipped



---



\## ▶️ How to Run the Project



\### Step 1: Clone the Repository

```bash

git clone https://github.com/<your-username>/sales-analytics-system.git

cd sales-analytics-system



Step 2: (Optional) Create Virtual Environment

python -m venv venv

source venv/bin/activate      # Windows: venv\\Scripts\\activate



Step 3: Install Dependencies

pip install -r requirements.txt



Step 4: Run the Program

python main.py



📤 Console Output (Validation Summary)

Total records parsed: 80

Invalid records removed: 10

Valid records after cleaning: 70



📊 Generated Output



output/sales\_report.txt



Total Revenue



Total Valid Transactions

