# Sales Analytics System

A Python-based sales data analytics system that cleans, validates, analyzes, enriches, and reports sales transactions using both local data and external APIs.

---

## Features

- Cleans and validates messy sales transaction data
- Performs revenue, region-wise, product-wise, and customer-wise analysis
- Identifies peak sales days and low-performing products
- Fetches product metadata from DummyJSON API
- Enriches sales data with API category, brand, and rating
- Generates detailed text-based analytical reports
- Supports optional user-driven data filtering via console input

---

## Project Structure

sales-analytics-system/
│
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt
│
├── output/
│ ├── summary.txt
│ └── sales_report.txt
│
└── utils/
├── data_processor.py
├── api_handler.py
└── file_handler.py


---

## Setup Instructions

1. Install dependencies:
pip install -r requirements.txt

2. Run the system:
python main.py


---

## Outputs Generated

- `output/summary.txt` – Revenue summary
- `data/enriched_sales_data.txt` – Sales data enriched using API
- `output/sales_report.txt` – Comprehensive analytics report

---

## External API Used

- DummyJSON Products API  
  https://dummyjson.com/products

---

## Notes

- All file paths are relative
- Errors are handled gracefully
- System runs end-to-end without crashing

---
