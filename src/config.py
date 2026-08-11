```python
from pathlib import Path


# ---------------------------------------------------------------------
# Project directories
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"


# ---------------------------------------------------------------------
# EPH temporal configuration
# ---------------------------------------------------------------------

START_YEAR = 2016

END_YEAR = 2025

EPH_QUARTERS = (1, 2, 3, 4)


# ---------------------------------------------------------------------
# EPH census framework
# ---------------------------------------------------------------------

# EPH observations up to 2024 use the census framework
# associated with the 2010 population census.
#
# From 2025 onwards, the new census framework associated
# with the 2022 population census is introduced.

CENSUS_REFERENCE_BEFORE_2025 = 2010

CENSUS_REFERENCE_FROM_2025 = 2022

CENSUS_CHANGE_YEAR = 2025


# ---------------------------------------------------------------------
# Economic variables
# ---------------------------------------------------------------------

# Variables that should be preserved in nominal terms and
# additionally transformed into real values using the
# selected deflator.

ECONOMIC_VARIABLES = (
    "ITF",
    "IPCF",
)


# ---------------------------------------------------------------------
# Deflator configuration
# ---------------------------------------------------------------------

# Base year for real monetary values.
#
# This is deliberately kept configurable rather than hard-coded
# throughout the processing pipeline.

DEFLATOR_BASE_YEAR = 2025
