import pandas as pd

def clean_ecommerce_data(file_path, output_path):
    print("🚀 Starting data cleaning process...")
    
    # 1. Load the dataset
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        print(f"✅ Data loaded successfully. Initial rows: {df.shape[0]}")
    except FileNotFoundError:
        print(f"❌ Error: The file at {file_path} was not found.")
        return

    # 2. Handle Missing Values
    df = df.dropna(subset=['CustomerID'])
    df['CustomerID'] = df['CustomerID'].astype(int)
    df['Description'] = df['Description'].fillna('Unknown Item')

    # 3. Fix Data Types & Clean Text
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df = df.dropna(subset=['InvoiceDate'])
    df['Description'] = df['Description'].str.strip()

    # 4. Filter Out Negative Quantities/Prices
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

    # 5. Feature Engineering (Calculate New Columns)
    df['Total_Sales'] = df['Quantity'] * df['UnitPrice']
    df['Year_Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)

    # 6. Drop Duplicates
    df = df.drop_duplicates()

    # 7. Export to Excel
    print(f"✨ Cleaning complete! Final rows: {df.shape[0]}")
    print(f"💾 Exporting clean data to {output_path}...")
    df.to_excel(output_path, index=False, sheet_name='Clean_Sales_Data')
    print("🎉 File successfully saved and ready for Excel Dashboarding!")

if __name__ == "__main__":
    INPUT_FILE = "raw_data.csv" 
    OUTPUT_FILE = "cleaned_sales_data.xlsx"
    clean_ecommerce_data(INPUT_FILE, OUTPUT_FILE)
