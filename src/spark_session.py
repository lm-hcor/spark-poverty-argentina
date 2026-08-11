from pyspark.sql import SparkSession


def create_spark_session() -> SparkSession:
    """Create and configure the Spark session."""

    return (
        SparkSession.builder
        .appName("ArgentinaPovertyAnalysis")
        .master("local[*]")
        .getOrCreate()
    )


if __name__ == "__main__":
    spark = create_spark_session()

    print("Spark version:", spark.version)
    print("Spark session created successfully.")

    spark.stop()