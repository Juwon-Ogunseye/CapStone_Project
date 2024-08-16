# Capstone Project

## Project Overview

This project is designed to automate and manage ETL (Extract, Transform, Load) processes using Apache Airflow. The project includes various services like PostgreSQL, Airflow, and custom Python scripts, all orchestrated using Docker Compose. The main purpose of the project is to efficiently manage and monitor data pipelines, ensuring data consistency and reliability.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Docker**: Make sure Docker is installed and running on your system.
- **Docker Compose**: This project uses Docker Compose to orchestrate multiple containers.
- **Python 3.9**: The project is based on Python 3.9.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Environment Variables**

   Create a `.env` file in the root directory with the necessary environment variables. Refer to the `.env` file template provided in the project.

3. **Build the Docker Containers**

   ```bash
   docker-compose build
   ```

4. **Start the Services**

   ```bash
   docker-compose up -d
   ```

5. **Accessing the Services**

   - **Airflow Webserver**: [http://localhost:8082](http://localhost:8082)
   - **PGAdmin**: [http://localhost:5002](http://localhost:5002)
   - **Python Script**: The script will run automatically within the container.

## Usage

### Running the Python Script

The `sandbox.py` script is executed automatically when the container starts. If you need to run it manually:

```bash
docker-compose run python-script
```

### Airflow

Airflow is used to orchestrate the ETL jobs. You can access the Airflow web interface to monitor and manage your DAGs.

### PostgreSQL & PGAdmin

The PostgreSQL database is used to store the data. PGAdmin is provided for database management and can be accessed via the browser.

### DBT Models and Transformations
## Fact Models
fct_avg_delivery_time: This model calculates the average delivery time across all orders. It uses the staged orders and order items data to compute the delivery time and aggregates it to provide an overall average.

fct_orders_by_state: Aggregates the number of orders per state, providing insights into which regions have the highest order volumes.

fct_sales_by_category: Aggregates sales data by product category, allowing analysis of revenue contribution from different categories.

Intermediate Models
int_avg_delivery_time: This intermediate model supports the calculation of average delivery time by preparing the necessary data from the staged models.

int_orders_by_state: This intermediate model prepares the data needed to calculate the number of orders by state, ensuring that the data is clean and well-structured before aggregation.

int_sales_by_category: This intermediate model prepares the sales data, organizing it by product category to facilitate easy aggregation in the fct_sales_by_category model.

Custom Models
my_first_dbt_model: This is an example model, likely used for initial testing or specific use cases within the project.

my_second_dbt_model: Similar to my_first_dbt_model, this is another custom model, used for specific tasks or demonstrations within the project.

Staging Models
staging_products: Stages the products data, ensuring it is clean and ready for further transformations and analysis.

stg_customers: Stages customer data, providing a clean and structured dataset for downstream models.

stg_order_items: Stages the order items data, preparing it for aggregation and analysis in other models.

stg_orders: Stages the orders data, ensuring that all date and time fields are properly cast and any necessary filtering is applied.

stg_products: Another model for staging product-related data, likely used in conjunction with staging_products.

Utility Models
verifynull: This model likely checks for null values in the dataset, ensuring data integrity and highlighting any missing or incomplete data that needs attention.

### Transformations

- **Date and Time Conversions**: Ensuring all date and time fields are properly cast and processed.
- **Data Integrity Checks**: Filtering out any records where date conversions fail or are invalid.

## Files and Directories

- **Dockerfile**: Defines the Docker image for the Python environment.
- **docker-compose.yml**: Orchestrates the Docker containers and services.
- **sandbox.py**: Main Python script for processing data.
- **etl_dags.py**: Contains the DAG definitions for Airflow.
- **functions.py**: Helper functions used across the project.
- **constant.py**: Stores constants used in the project.
- **.env**: Environment variables file (not included, needs to be created).

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or need further assistance, please reach out to:

- **Your Name**
- **Email:** [your.email@example.com](mailto:your.email@example.com)

---

Feel free to replace placeholders like `<repository-url>` and `<repository-directory>` with actual values. You can also expand on the model explanations and transformations as needed.