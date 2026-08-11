from src.config import RAW_DATA_DIR
from src.spark_session import create_spark_session


def main():
    spark = create_spark_session()

    individual_path = (
        RAW_DATA_DIR
        / "eph"
        / "2025"
        / "eph_individual_2025_q4.parquet"
    )

    household_path = (
        RAW_DATA_DIR
        / "eph"
        / "2025"
        / "eph_hogar_2025_q4.parquet"
    )

    # ------------------------------------------------------------------
    # Load datasets
    # ------------------------------------------------------------------

    individual = spark.read.parquet(str(individual_path))
    household = spark.read.parquet(str(household_path))

    print("\n=== INPUT DATASETS ===")
    print(f"Individual rows: {individual.count()}")
    print(f"Household rows: {household.count()}")

    # ------------------------------------------------------------------
    # Validate household keys
    # ------------------------------------------------------------------

    household_keys = household.select(
        "CODUSU",
        "NRO_HOGAR",
    )

    print("\n=== HOUSEHOLD KEY VALIDATION ===")

    duplicate_keys = (
        household_keys
        .groupBy("CODUSU", "NRO_HOGAR")
        .count()
        .filter("count > 1")
    )

    duplicate_count = duplicate_keys.count()

    print(f"Duplicate household keys: {duplicate_count}")

    null_keys = household.filter(
        "CODUSU IS NULL OR NRO_HOGAR IS NULL"
    ).count()

    print(f"Households with null keys: {null_keys}")

    # ------------------------------------------------------------------
    # Select household-level variables
    #
    # Rename variables that also exist in the individual database
    # to avoid ambiguous references after the join.
    # ------------------------------------------------------------------

    household_selected = (
        household.select(
            "CODUSU",
            "NRO_HOGAR",
            "PONDIH",
            "IV1",
            "IV2",
            "IV3",
            "IV4",
            "IV5",
            "IV6",
            "IV7",
            "IV8",
            "IV9",
            "IV10",
            "IV11",
            "ITF",
            "IPCF",
            "IX_TOT",
            "IX_MEN10",
            "IX_MAYEQ10",
        )
        .withColumnRenamed(
            "PONDIH",
            "PONDIH_HOGAR",
        )
        .withColumnRenamed(
            "ITF",
            "ITF_HOGAR",
        )
        .withColumnRenamed(
            "IPCF",
            "IPCF_HOGAR",
        )
    )

    # ------------------------------------------------------------------
    # Join Individual + Household
    # ------------------------------------------------------------------

    enriched = individual.join(
        household_selected,
        on=["CODUSU", "NRO_HOGAR"],
        how="left",
    )

    print("\n=== JOIN RESULT ===")

    joined_rows = enriched.count()

    print(f"Joined rows: {joined_rows}")

    # ------------------------------------------------------------------
    # Check unmatched individuals
    # ------------------------------------------------------------------

    unmatched = (
        enriched
        .filter("PONDIH_HOGAR IS NULL")
        .count()
    )

    print(
        "Individuals without household match: "
        f"{unmatched}"
    )

    # ------------------------------------------------------------------
    # Show enriched sample
    # ------------------------------------------------------------------

    print("\n=== ENRICHED SAMPLE ===")

    enriched.select(
        "CODUSU",
        "NRO_HOGAR",
        "COMPONENTE",
        "ANO4",
        "TRIMESTRE",
        "REGION",
        "AGLOMERADO",
        "PONDERA",
        "PONDIH",
        "PONDIH_HOGAR",
        "ITF",
        "ITF_HOGAR",
        "IPCF",
        "IPCF_HOGAR",
        "IV1",
        "IV2",
        "IV3",
    ).show(
        10,
        truncate=False,
    )

    spark.stop()


if __name__ == "__main__":
    main()