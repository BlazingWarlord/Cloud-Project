import boto3
import pyodbc

# AWS RDS credentials
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
aws_region = 'us-west-2'  # Replace with your AWS region

# Azure SQL Database credentials
azure_sql_server = 'YOUR_AZURE_SQL_SERVER'
azure_sql_database = 'YOUR_AZURE_SQL_DATABASE'
azure_sql_username = 'YOUR_AZURE_SQL_USERNAME'
azure_sql_password = 'YOUR_AZURE_SQL_PASSWORD'

# AWS RDS instance details
aws_rds_instance_id = 'YOUR_AWS_RDS_INSTANCE_ID'

# Connect to AWS RDS SQL Server
session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
client = session.client('rds')
response = client.describe_db_instances(DBInstanceIdentifier=aws_rds_instance_id)
aws_db_instance = response['DBInstances'][0]

# Extract data from AWS RDS SQL Server
aws_db_endpoint = aws_db_instance['Endpoint']['Address']
aws_db_username = aws_db_instance['MasterUsername']
aws_db_password = 'YOUR_AWS_RDS_MASTER_PASSWORD'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={aws_db_endpoint};DATABASE=master;UID={aws_db_username};PWD={aws_db_password}'

# Connect to Azure SQL Database
azure_connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={azure_sql_server}.database.windows.net;DATABASE={azure_sql_database};UID={azure_sql_username};PWD={azure_sql_password}'

# Extract data from AWS and import it into Azure
with pyodbc.connect(connection_string) as aws_conn:
    with pyodbc.connect(azure_connection_string) as azure_conn:
        aws_cursor = aws_conn.cursor()
        azure_cursor = azure_conn.cursor()

        # Extract data from AWS RDS SQL Server
        aws_cursor.execute('SELECT * FROM YourTable')
        rows = aws_cursor.fetchall()

        # Import data into Azure SQL Database
        for row in rows:
            azure_cursor.execute('INSERT INTO YourTable (Column1, Column2) VALUES (?, ?)', row.Column1, row.Column2)

print('SQL server migration from AWS to Azure completed.')



