from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "cpi"
    / "serie_ipc_aperturas.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "economic"
)

OUTPUT_FILE = OUTPUT_DIR / "regional_cpi.parquet"


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

BASE_YEAR = 2016
BASE_PERIOD = 201612

TARGET_REGIONS = [
    "GBA",
    "Pampeana",
    "Noreste",
    "Noroeste",
    "Cuyo",
    "Patagonia",
]


# ---------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------

def load_cpi() -> pd.DataFrame:
    """
    Load the official INDEC regional CPI series.
    """

    df = pd.read_csv(
        INPUT_FILE,
        encoding="cp1252",
        sep=";",
    )

    return df


# ---------------------------------------------------------------------
# Filter
# ---------------------------------------------------------------------

def prepare_cpi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep the regional headline CPI and standardize temporal fields.
    """

    df = df.copy()

    # Normalize period
    df["Periodo"] = df["Periodo"].astype(str).str.strip()
    df["year"] = df["Periodo"].str[:4].astype(int)
    df["month"] = df["Periodo"].str[4:6].astype(int)

    # Numeric CPI
    df["Indice_IPC"] = pd.to_numeric(
        df["Indice_IPC"],
        errors="coerce",
    )

    # Keep only headline CPI
    df = df[
        df["Descripcion_aperturas"].str.strip()
        == "Nivel general"
    ]

    # Keep relevant regions
    df = df[
        df["Region"].isin(TARGET_REGIONS)
    ]

    # Keep relevant period
    df = df[
        df["year"] >= BASE_YEAR
    ]

    return df


# ---------------------------------------------------------------------
# Build quarterly CPI
# ---------------------------------------------------------------------

def build_quarterly_cpi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert monthly regional CPI into quarterly averages.

    The EPH is quarterly, therefore the CPI is aggregated using
    the arithmetic mean of the three monthly indices.
    """

    df = df.copy()

    df["quarter"] = ((df["month"] - 1) // 3) + 1

    quarterly = (
        df.groupby(
            ["year", "quarter", "Region"],
            as_index=False,
        )["Indice_IPC"]
        .mean()
        .rename(
            columns={
                "Indice_IPC": "cpi_quarterly"
            }
        )
    )

    return quarterly


# ---------------------------------------------------------------------
# Build 2016-base deflator
# ---------------------------------------------------------------------

def build_deflator(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct a regional CPI index relative to the 2016 base.

    The CPI dataset is already expressed with December 2016 = 100.
    We nevertheless explicitly calculate the regional base so that
    the transformation remains transparent and auditable.
    """

    df = df.copy()

    # Regional December 2016 base
    base = (
        df[
            (df["year"] == BASE_YEAR)
            & (df["month"] == 12)
        ]
        .groupby("Region", as_index=False)["Indice_IPC"]
        .mean()
        .rename(
            columns={
                "Indice_IPC": "cpi_base_2016"
            }
        )
    )

    df = df.merge(
        base,
        on="Region",
        how="left",
        validate="many_to_one",
    )

    # Index relative to December 2016
    df["cpi_index_2016"] = (
        df["Indice_IPC"]
        / df["cpi_base_2016"]
    ) * 100

    # Deflator that converts nominal values into 2016 prices
    df["deflator_2016"] = (
        df["cpi_base_2016"]
        / df["Indice_IPC"]
    )

    return df


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("Loading INDEC regional CPI...")

    df = load_cpi()

    print(f"Raw rows: {len(df):,}")

    df = prepare_cpi(df)

    print(f"Filtered rows: {len(df):,}")

    # Monthly dataset
    monthly = build_deflator(df)

    quarterly = build_quarterly_cpi(
        monthly
    )

    # Quarterly regional base
    quarterly_base = (
        quarterly[
            (quarterly["year"] == 2016)
            & (quarterly["quarter"] == 4)
        ]
        .groupby("Region", as_index=False)["cpi_quarterly"]
        .mean()
        .rename(
            columns={
                "cpi_quarterly":
                "cpi_quarterly_base_2016"
            }
        )
    )

    quarterly = quarterly.merge(
        quarterly_base,
        on="Region",
        how="left",
        validate="many_to_one",
    )

    quarterly["cpi_index_2016"] = (
        quarterly["cpi_quarterly"]
        / quarterly["cpi_quarterly_base_2016"]
    ) * 100

    quarterly["deflator_2016"] = (
        quarterly["cpi_quarterly_base_2016"]
        / quarterly["cpi_quarterly"]
    )

    # Save
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    quarterly.to_parquet(
        OUTPUT_FILE,
        index=False,
    )

    print()
    print("=== REGIONAL CPI ===")
    print(f"Rows: {len(quarterly):,}")
    print(
        f"Years: "
        f"{quarterly['year'].min()}-"
        f"{quarterly['year'].max()}"
    )

    print()
    print("Regions:")
    print(
        quarterly["Region"]
        .drop_duplicates()
        .sort_values()
        .to_list()
    )

    print()
    print("Sample:")
    print(
        quarterly.head(12).to_string(
            index=False
        )
    )

    print()
    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()