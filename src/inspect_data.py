from src.config import RAW_DATA_DIR
from src.spark_session import create_spark_session


def main():
    spark = create_spark_session()

    path = (
        RAW_DATA_DIR
        / "eph"
        / "2025"
        / "eph_individual_2025_q4.parquet"
    )

    df = spark.read.parquet(str(path))

    print("\n=== EPH DATASET ===")
    print(f"Rows: {df.count()}")
    print(f"Columns: {len(df.columns)}")

    print("\n=== SAMPLE ===")
    df.select(
        "CODUSU",
        "ANO4",
        "TRIMESTRE",
        "REGION",
        "AGLOMERADO",
        "PONDERA",
        "CH04",
        "CH06",
        "NIVEL_ED",
        "ESTADO",
        "ITF",
        "IPCF",
    ).show(10, truncate=False)

    print("\n=== SCHEMA ===")
    df.printSchema()

    spark.stop()


if __name__ == "__main__":
    main()