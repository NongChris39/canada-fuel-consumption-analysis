from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "my2015-2024-fuel-consumption-ratings.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"
TARGET_COLUMN = "Combined (L/100 km)"

COLUMNS_TO_DROP = [
    "Combined (mpg)",
    "CO2 emissions (g/km)",
    "CO2 rating",
    "Smog rating",
]
