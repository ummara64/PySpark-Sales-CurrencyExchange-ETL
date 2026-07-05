# ==========================================
# config.py
# ==========================================

import os

# Base Project Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input Files
SALES_FILE = os.path.join(BASE_DIR, "data", "sales_data 2.csv")
PRODUCT_FILE = os.path.join(BASE_DIR, "data", "product_reference 2.csv")

# Output
REJECTED_RECORDS = os.path.join(BASE_DIR, "logs", "rejected_records")

# Logging
LOG_FILE = os.path.join(BASE_DIR, "logs", "pipeline.log")

# API
EXCHANGE_RATE_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Pipeline
ERROR_THRESHOLD = 5

# SQL Server
# JDBC_URL = "jdbc:sqlserver://localhost:1433;databaseName=SalesDB"
JDBC_URL = (
    "jdbc:sqlserver://localhost:1433;"
    "databaseName=SalesETL;"
    "encrypt=true;"
    "trustServerCertificate=true;"
)
DB_PROPERTIES = {
    "user": "sa",
    "password": "Test@12345",   
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}