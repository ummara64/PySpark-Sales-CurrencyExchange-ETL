# ==========================================
# database.py
# ==========================================

from utils.config import JDBC_URL
from utils.config import DB_PROPERTIES
from pyspark.sql.functions import to_json, struct

def write_fact_sales(df):

    (
        df.write
        .mode("append")
        .jdbc(
            url=JDBC_URL,
            table="FactSales",
            properties=DB_PROPERTIES
        )
    )



def write_rejected_records(df):

    rejected = (

        df.withColumn(
            "RecordData",
            to_json(struct(*df.columns))
        )

        .select(
            "OrderID",
            "ProductID",
            "CustomerID",
            "RejectReason",
            "RecordData"
        )

    )

    (

        rejected.write

        .mode("append")

        .jdbc(
            url=JDBC_URL,
            table="RejectedRecords",
            properties=DB_PROPERTIES
        )

    )

def write_currency_log(df):

    conversion_log = (

        df.select(

            "OrderID",

            "Currency",

            "ExchangeRate",

            "SaleAmount",

            "SaleAmountUSD",

            "ConversionTimestamp"

        )

    )

    (

        conversion_log.write

        .mode("append")

        .jdbc(

            url=JDBC_URL,

            table="CurrencyConversionLog",

            properties=DB_PROPERTIES

        )

    )

def write_error_log(df):

    (
        df.write
        .mode("append")
        .jdbc(
            url=JDBC_URL,
            table="ErrorLog",
            properties=DB_PROPERTIES
        )
    )
   