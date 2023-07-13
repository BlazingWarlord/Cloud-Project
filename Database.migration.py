#pip install pyodbc
import pyodbc

# Define connection details for the source database
source_driver = "{your_driver}"
source_server = "your_server"
source_database = "your_database"
source_username = "your_username"
source_password = "your_password"

# Define connection details for the Azure SQL Database
azure_driver = "{ODBC Driver 17 for SQL Server}"
azure_server = "your_server_name.database.windows.net"
azure_database = "your_database_name"
azure_username = "your_username"
azure_password = "your_password"

# Establish connection to the source database
source_connection_string = f"DRIVER={source_driver};SERVER={source_server};DATABASE={source_database};UID={source_username};PWD={source_password}"
source_connection = pyodbc.connect(source_connection_string)

# Establish connection to the Azure SQL Database
azure_connection_string = f"DRIVER={azure_driver};SERVER={azure_server};DATABASE={azure_database};UID={azure_username};PWD={azure_password}"
azure_connection = pyodbc.connect(azure_connection_string)

# Define the table to migrate
source_table_name = "your_source_table_name"
azure_table_name = "your_azure_table_name"

try:
    # Fetch data from the source table
    source_cursor = source_connection.cursor()
    source_cursor.execute(f"SELECT * FROM {source_table_name}")
    rows = source_cursor.fetchall()

    # Insert data into the Azure SQL Database table
    azure_cursor = azure_connection.cursor()
    for row in rows:
        azure_cursor.execute(f"INSERT INTO {azure_table_name} (column1, column2, ...) VALUES (?, ?, ...)", row)
    azure_connection.commit()

    print("Migration completed successfully!")
except Exception as e:
    print("An error occurred during migration:", e)
finally:
    # Close connections
    source_connection.close()
    azure_connection.close()
