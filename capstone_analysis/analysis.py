from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from dotenv import load_dotenv
import os
import constant  # Import the constants

# Load environment variables from .env file
load_dotenv()

# Set up Google Cloud authentication
GOOGLE_AUTH_FILE = os.getenv('GOOGLE_AUTH_FILE_ANALYSIS')
if not GOOGLE_AUTH_FILE:
    raise ValueError("The environment variable GOOGLE_AUTH_FILE_ANALYSIS is not set.")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_AUTH_FILE

# Set up BigQuery client
client = bigquery.Client()

# Queries using the existing views
queries = {
    "avg_delivery_time": f"SELECT * FROM `{constant.PROJECT_ID}.{constant.DATASET_ID}.fct_avg_delivery_time`",
    "orders_by_state": f"SELECT * FROM `{constant.PROJECT_ID}.{constant.DATASET_ID}.fct_orders_by_state`",
    "sales_by_category": f"SELECT * FROM `{constant.PROJECT_ID}.{constant.DATASET_ID}.fct_sales_by_category`"
}

# Fetch data into DataFrames
dataframes = {name: client.query(query).to_dataframe() for name, query in queries.items()}

# Check for missing values in the 'product_category_name' column
if dataframes['sales_by_category']['product_category_name'].isnull().any():
    print("Warning: There are missing values in the product_category_name column.")
    # Drop rows with missing product_category_name
    dataframes['sales_by_category'] = dataframes['sales_by_category'].dropna(subset=['product_category_name'])

# Set the size of the PDF pages to be wider
pdf_width, pdf_height = 14, 8.5  # Setting width to 14 inches

# Create a PdfPages object to save plots
with PdfPages('dashboard_report.pdf') as pdf:
    
    # Adding the header to the PDF
    fig, ax = plt.subplots(figsize=(pdf_width, 1.5))
    ax.set_axis_off()
    header_text = (
        "Project Title: Data Engineering Capstone Projects\n"
        "Designer Title: Data Engineer\n"
        "School Name: Alt School\n"
        "Data Engineer: Ogunseye Oluwajuwon Micheal\n"
        "Dataset: Brazilian E-Commerce Dataset"
    )
    plt.text(0.5, 0.5, header_text, ha='center', va='center', fontsize=14, weight='bold', transform=ax.transAxes)
    pdf.savefig(fig)
    plt.close()

    # 1. Average Delivery Time
    avg_delivery_time = dataframes['avg_delivery_time']['avg_delivery_time_days'].iloc[0]
    fig, ax = plt.subplots(figsize=(pdf_width, 2))
    ax.set_axis_off()
    plt.text(0.5, 0.5, f"Average Delivery Time: {avg_delivery_time:.2f} days", ha='center', va='center', fontsize=16, weight='bold', transform=ax.transAxes)
    pdf.savefig(fig)
    plt.close()

    # 2. States with the Highest Number of Orders - Bar Chart
    orders_by_state = dataframes['orders_by_state'].sort_values(by='total_orders', ascending=False)
    plt.figure(figsize=(pdf_width, 6))
    plt.bar(orders_by_state['customer_state'], orders_by_state['total_orders'], color='skyblue')
    plt.title('Number of Orders by State')
    plt.xlabel('State')
    plt.ylabel('Total Orders')
    pdf.savefig()
    plt.close()

    # 3. Product Categories with the Highest Sales - Top 20 Visualization
    sales_by_category = dataframes['sales_by_category'].sort_values(by='total_sales', ascending=False).head(20)
    plt.figure(figsize=(pdf_width, 6))
    plt.barh(sales_by_category['product_category_name'], sales_by_category['total_sales'], color='lightgreen')
    plt.title('Top 20 Sales by Product Category')
    plt.xlabel('Total Sales')
    plt.ylabel('Product Category')
    pdf.savefig()
    plt.close()

    # 4. Number of Orders by State - Simplified Map Visualization
    # Create a simplified DataFrame with approximate lat/long for each Brazilian state
    state_coords = {
        'customer_state': ['SP', 'RJ', 'MG', 'RS', 'PR', 'BA', 'SC', 'GO', 'ES', 'DF'],
        'latitude': [-23.5505, -22.9068, -19.9167, -30.0346, -25.4297, -12.9714, -27.5954, -15.7801, -19.0197, -15.8267],
        'longitude': [-46.6333, -43.1729, -43.9345, -51.2177, -49.2733, -38.5014, -48.548, -47.9292, -40.3363, -47.9218]
    }
    state_coords_df = pd.DataFrame(state_coords)

    # Merge with orders data
    orders_map_data = pd.merge(state_coords_df, orders_by_state, on='customer_state', how='left')
    orders_map_data['total_orders'] = orders_map_data['total_orders'].fillna(0)  # Replace NaN with 0

    # Plot the map
    plt.figure(figsize=(pdf_width, 8))
    plt.scatter(orders_map_data['longitude'], orders_map_data['latitude'], s=orders_map_data['total_orders'] * 10, color='red', alpha=0.6, edgecolors="k")
    plt.title('Number of Orders by State - Map View')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    for i, row in orders_map_data.iterrows():
        plt.text(row['longitude'], row['latitude'], row['customer_state'], fontsize=12, ha='center')
    pdf.savefig()
    plt.close()

# Display the sorted dataframes for reference in the console
print("\nStates with the highest number of orders:")
print(orders_by_state)

print("\nTop 20 product categories with the highest sales:")
print(sales_by_category)
