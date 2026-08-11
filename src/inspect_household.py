from src.config import RAW_DATA_DIR
from src.spark_session import create_spark_session


def main():
    spark = create_spark_session()

    path = (
        RAW_DATA_DIR
        / "eph"
        / "2025"
        / "eph_hogar_2025_q4.parquet"
    )

    df = spark.read.parquet(str(path))

    print("\n=== HOUSEHOLD DATASET ===")
    print(f"Rows: {df.count()}")
    print(f"Columns: {len(df.columns)}")

    print("\n=== COLUMNS ===")
    print(df.columns)

    print("\n=== SCHEMA ===")
    df.printSchema()

    print("\n=== SAMPLE ===")
    df.show(5, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()