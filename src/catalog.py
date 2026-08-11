from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_DIR


def build_catalog() -> pd.DataFrame:
    """
    Build a catalog of all EPH Parquet files available
    in the raw data directory.
    """

    eph_dir = RAW_DATA_DIR / "eph"

    records = []

    for path in sorted(eph_dir.rglob("*.parquet")):

        filename = path.name

        # Expected format:
        # eph_individual_2025_q4.parquet
        # eph_hogar_2025_q4.parquet

        parts = filename.replace(
            ".parquet",
            "",
        ).split("_")

        if len(parts) != 4:
            continue

        _, base_type, year, quarter = parts

        records.append(
            {
                "year": int(year),
                "quarter": int(
                    quarter.replace("q", "")
                ),
                "base_type": base_type,
                "path": str(path),
                "size_mb": round(
                    path.stat().st_size
                    / (1024 ** 2),
                    2,
                ),
            }
        )

    catalog = pd.DataFrame(records)

    if catalog.empty:
        return catalog

    catalog = catalog.sort_values(
        [
            "year",
            "quarter",
            "base_type",
        ]
    ).reset_index(drop=True)

    return catalog


def main():

    catalog = build_catalog()

    print("\n=== EPH DATA CATALOG ===")

    if catalog.empty:
        print("No Parquet files found.")
        return

    print(
        f"Total files: {len(catalog)}"
    )

    print(
        f"Years: "
        f"{catalog['year'].min()}-"
        f"{catalog['year'].max()}"
    )

    print(
        f"Total size: "
        f"{catalog['size_mb'].sum():,.2f} MB"
    )

    print("\n=== FILES BY YEAR ===")

    yearly = (
        catalog
        .groupby("year")
        .agg(
            files=("path", "count"),
            size_mb=("size_mb", "sum"),
        )
        .reset_index()
    )

    print(yearly.to_string(index=False))

    print("\n=== MISSING PERIODS ===")

    expected = {
        (year, quarter, base_type)
        for year in range(
            catalog["year"].min(),
            catalog["year"].max() + 1,
        )
        for quarter in range(1, 5)
        for base_type in (
            "individual",
            "hogar",
        )
    }

    actual = set(
        zip(
            catalog["year"],
            catalog["quarter"],
            catalog["base_type"],
        )
    )

    missing = sorted(expected - actual)

    if not missing:
        print("No missing datasets.")
    else:
        for item in missing:
            print(item)

    output_path = (
        RAW_DATA_DIR
        / "eph_catalog.csv"
    )

    catalog.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nCatalog saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()

