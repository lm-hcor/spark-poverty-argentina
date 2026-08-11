import argparse
from pathlib import Path

import pyeph

from src.config import RAW_DATA_DIR


VALID_BASE_TYPES = {"individual", "hogar"}
VALID_PERIODS = {1, 2, 3, 4}


def get_output_path(
    year: int,
    period: int,
    base_type: str,
) -> Path:
    """Return the output path for an EPH Parquet dataset."""

    output_dir = RAW_DATA_DIR / "eph" / str(year)
    output_dir.mkdir(parents=True, exist_ok=True)

    return (
        output_dir
        / f"eph_{base_type}_{year}_q{period}.parquet"
    )


def download_eph(
    year: int,
    period: int,
    base_type: str,
) -> tuple[str, Path | None]:
    """
    Download one EPH-INDEC dataset.

    Returns
    -------
    tuple
        Status ('downloaded', 'exists', 'failed')
        and output path when available.
    """

    if base_type not in VALID_BASE_TYPES:
        raise ValueError(
            f"Invalid base_type: {base_type}"
        )

    if period not in VALID_PERIODS:
        raise ValueError(
            f"Invalid period: {period}"
        )

    output_path = get_output_path(
        year,
        period,
        base_type,
    )

    # Avoid downloading files that already exist.
    if output_path.exists():
        print(
            f"[EXISTS] {base_type} "
            f"{year} Q{period}"
        )
        return "exists", output_path

    print(
        f"[DOWNLOAD] {base_type} "
        f"{year} Q{period}"
    )

    try:
        data = pyeph.get(
            data="eph",
            year=year,
            period=period,
            base_type=base_type,
        )

        data.to_parquet(
            output_path,
            index=False,
        )

        print(
            f"[SAVED] {output_path}"
        )

        return "downloaded", output_path

    except Exception as exc:
        print(
            f"[FAILED] {base_type} "
            f"{year} Q{period}: {exc}"
        )

        return "failed", None


def download_year(
    year: int,
) -> dict[str, int]:
    """Download both EPH bases for all four quarters."""

    summary = {
        "downloaded": 0,
        "exists": 0,
        "failed": 0,
    }

    for period in sorted(VALID_PERIODS):

        for base_type in (
            "individual",
            "hogar",
        ):
            status, _ = download_eph(
                year=year,
                period=period,
                base_type=base_type,
            )

            summary[status] += 1

    return summary


def download_range(
    start_year: int,
    end_year: int,
) -> dict[str, int]:
    """Download EPH data for a range of years."""

    total_summary = {
        "downloaded": 0,
        "exists": 0,
        "failed": 0,
    }

    for year in range(
        start_year,
        end_year + 1,
    ):

        print(
            "\n"
            + "=" * 60
        )

        print(
            f"YEAR {year}"
        )

        print(
            "=" * 60
        )

        summary = download_year(year)

        for key in total_summary:
            total_summary[key] += summary[key]

        print(
            f"Year {year} summary: "
            f"{summary}"
        )

    return total_summary


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Download EPH-INDEC "
            "microdata using PyEPH."
        )
    )

    parser.add_argument(
        "--start-year",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--end-year",
        type=int,
        required=True,
    )

    args = parser.parse_args()

    if args.start_year > args.end_year:
        raise ValueError(
            "start-year must be <= end-year"
        )

    print("\nEPH DOWNLOAD PIPELINE")
    print(
        f"Years: "
        f"{args.start_year}-{args.end_year}"
    )
    print(
        "Bases: individual + hogar"
    )
    print(
        "Periods: Q1-Q4"
    )

    summary = download_range(
        args.start_year,
        args.end_year,
    )

    print(
        "\n"
        + "=" * 60
    )

    print("FINAL DOWNLOAD SUMMARY")

    print(
        f"Downloaded: "
        f"{summary['downloaded']}"
    )

    print(
        f"Already existed: "
        f"{summary['exists']}"
    )

    print(
        f"Failed: "
        f"{summary['failed']}"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":
    main()
