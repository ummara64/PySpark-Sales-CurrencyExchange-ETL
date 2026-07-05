# ==========================================
# exchange_rate.py
# ==========================================

import requests
import logging

from pyspark.sql.functions import (
    broadcast,
    col,
    round,
    current_timestamp
)

from utils.config import EXCHANGE_RATE_URL


def fetch_exchange_rates():
    """
    Fetch exchange rates from external API.
    Falls back to default rates if API is unavailable.
    """

    try:
        response = requests.get(EXCHANGE_RATE_URL, timeout=10)
        response.raise_for_status()

        rates = response.json()["rates"]

        logging.info("Exchange rates fetched successfully.")

        return rates

    except Exception as ex:

        logging.error(f"Exchange Rate API failed: {str(ex)}")

        # Default fallback rates
        return {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79
        }


def create_exchange_rate_df(spark, rates):
    """
    Convert dictionary of exchange rates into Spark DataFrame.
    """

    exchange_rate_list = [
        (currency, float(rate))
        for currency, rate in rates.items()
    ]

    exchange_df = spark.createDataFrame(
        exchange_rate_list,
        ["Currency", "ExchangeRate"]
    )

    return exchange_df


def convert_to_usd(sales_df, exchange_df):
    """
    Join exchange rates and convert SaleAmount to USD.
    """

    enriched_df = (

        sales_df

        .join(
            broadcast(exchange_df),
            on="Currency",
            how="left"
        )

        .withColumn(
            "SaleAmountUSD",
            round(
                col("SaleAmount") / col("ExchangeRate"),
                2
            )
        )

        .withColumn(
            "ConversionTimestamp",
            current_timestamp()
        )

    )

    logging.info("Currency conversion completed.")

    return enriched_df