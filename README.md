# Senior Data Engineer – Technical Assessment

## Project structure
```
Senior Data Engineer - Test/
├── Notebooks/
│   ├── ETL_Pipeline.ipynb
├── utils/
│   ├── config.py
│   ├── database.py
│   ├── exchange_rate.py
│   ├── logger.py
│   └── validation.py
├── sql/
│   ├── create_db.sql
│   └── create_tables.sql
├── data/
│   └── product_reference 2.csv
├── Diagrams/
│   ├── High Level Architecture.png
│   └── Low Level architecture.png
└── .gitignore
```

## Pipeline (Notebooks/ETL_Pipeline.ipynb)
1. Starts a local Spark session (`Senior DE - ETL`).
2. Reads `sales_data 2.csv` and `product_reference 2.csv` from `data/` with header and schema inference.
3. Cleaning: drops duplicate `OrderID` rows, fills null `Discount` with `0`.
4. Validation (`validate_sales`): splits rows into `valid_df` and `rejected_df`, rejecting rows where:
   - `OrderID` is missing
   - `ProductID` is missing
   - `SaleAmount` is missing or `<= 0`
   - `Currency` is missing or not one of `USD`, `EUR`, `GBP`
   - `OrderDate` is missing
5. Standardizes `OrderDate` into a timestamp, trying formats `dd/MM/yyyy`, `dd-MM-yyyy`, `yyyy-MM-dd` in order.
6. Left-joins `valid_df` with `product_reference` (broadcast join) on `ProductID` to add `ProductName` and `Category`.
7. Fetches live exchange rates from `https://api.exchangerate-api.com/v4/latest/USD`; on failure, falls back to hardcoded rates (`USD: 1.0`, `EUR: 0.92`, `GBP: 0.79`).
8. Converts `SaleAmount` to `SaleAmountUSD` using the fetched rate and adds a `ConversionTimestamp`.
9. Writes results via JDBC:
   - `valid_df` → `FactSales`
   - `rejected_df` → `RejectedRecords`
   - currency conversion fields from `valid_df` → `CurrencyConversionLog`

## utils/
- **config.py** – file paths (`SALES_FILE`, `PRODUCT_FILE`), `REJECTED_RECORDS` path, `LOG_FILE` path, `EXCHANGE_RATE_URL`, `ERROR_THRESHOLD = 5`, SQL Server `JDBC_URL` and `DB_PROPERTIES` (user/password/driver).
- **logger.py** – `setup_logger()` configures logging to `logs/pipeline.log`.
- **validation.py** – `validate_sales(df)`, rules listed above.
- **exchange_rate.py** – `fetch_exchange_rates()`, `create_exchange_rate_df()`, `convert_to_usd()`.
- **database.py** – `write_fact_sales()`, `write_rejected_records()`, `write_currency_log()`, `write_error_log()` (all write via JDBC to SQL Server).

## Database schema (sql/create_tables.sql)
- **FactSales** – `OrderID` (PK), `ProductID`, `ProductName`, `Category`, `CustomerID`, `Region`, `OrderDate`, `SaleAmount`, `Currency`, `ExchangeRate`, `SaleAmountUSD`, `Discount`, `ConversionTimestamp`, `LoadTimestamp`
- **RejectedRecords** – `RejectID` (PK), `OrderID`, `ProductID`, `CustomerID`, `RejectReason`, `RecordData`, `RejectedAt`
- **CurrencyConversionLog** – `ConversionID` (PK), `OrderID`, `Currency`, `ExchangeRate`, `SaleAmount`, `SaleAmountUSD`, `ConversionTimestamp`
- **ErrorLog** – `ErrorID` (PK), `ErrorType`, `ErrorMessage`, `RecordID`, `ErrorTimestamp`

`sql/create_db.sql` creates the `SalesETL` database.

## Diagrams
- `Diagrams/High Level Architecture.png` – high-level architecture diagram
- `Diagrams/Low Level architecture.png` – low-level architecture diagram

## Setup & run steps
1. Run `sql/create_db.sql` on SQL Server, then run `sql/create_tables.sql` against the `SalesETL` database.
2. Place `sales_data 2.csv` and `product_reference 2.csv` in the `data/` folder.
3. Update `JDBC_URL` and `DB_PROPERTIES` in `utils/config.py` if your SQL Server connection details differ.
4. Open `Notebooks/ETL_Pipeline.ipynb` and run all cells (requires PySpark and the SQL Server JDBC driver available to Spark).
5. Pipeline logs are written to `Notebooks/logs/pipeline.log` (per `LOG_FILE` in config.py, relative to the notebook's working directory).
