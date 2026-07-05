from pyspark.sql.functions import col, when


def validate_sales(df):
    """
    Validates sales records and separates valid and rejected records.

    Returns:
        valid_df
        rejected_df
    """

    validated_df = (
        df.withColumn(
            "RejectReason",
            when(col("OrderID").isNull(), "Missing OrderID")
            .when(col("ProductID").isNull(), "Missing ProductID")
            .when(col("SaleAmount").isNull(), "Missing SaleAmount")
            .when(col("SaleAmount") <= 0, "Invalid SaleAmount")
            .when(col("Currency").isNull(), "Missing Currency")
            .when(~col("Currency").isin("USD", "EUR", "GBP"), "Unsupported Currency")
            .when(col("OrderDate").isNull(), "Invalid OrderDate")
            .otherwise(None)
        )
    )

    valid_df = validated_df.filter(col("RejectReason").isNull())

    rejected_df = validated_df.filter(col("RejectReason").isNotNull())

    return valid_df, rejected_df