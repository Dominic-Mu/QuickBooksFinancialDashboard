# QuickBooks Financial Dashboard

An interactive financial dashboard for analyzing QuickBooks data.

## Setup

1. Clone this repository
2. Create a virtual environment:   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate   ```
3. Install requirements:   ```bash
   pip install -r requirements.txt   ```

## Running the Dashboard

1. Navigate to the project directory
2. Run the Streamlit app:   ```bash
   streamlit run src/app.py   ```
3. Open your browser and go to http://localhost:8501

## Data Format Requirements

The uploaded CSV or Excel file should contain the following columns:
- Date: Transaction date
- Amount: Transaction amount
- Category: Transaction category
- Type: Either 'Revenue' or 'Expense'

## Features

- Interactive data upload
- Date range filtering
- Category filtering
- Revenue and expense tracking
- Visual representations of financial data
- Downloadable reports 