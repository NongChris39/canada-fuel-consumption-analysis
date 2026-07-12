from pathlib import Path
import pandas as pd

def load_dataset(csv_path: Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path.resolve()}")
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("The dataset is empty.")
    return df
