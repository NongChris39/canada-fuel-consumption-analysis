import numpy as np
import pandas as pd

def evaluate_data_quality(df: pd.DataFrame) -> dict:
    completeness = float((1 - df.isna().mean()).mean())
    rules = {
        "valid_model_year": float(df["Model year"].between(2015, 2024).mean()),
        "valid_engine_size": float(df["Engine size (L)"].between(0.5, 10.0).mean()),
        "valid_cylinders": float(df["Cylinders"].between(2, 16).mean()),
        "valid_consumption": float(df["Combined (L/100 km)"].between(2.0, 30.0).mean()),
        "highway_combined_city_consistency": float(
            (
                (df["Highway (L/100 km)"] < df["Combined (L/100 km)"])
                & (df["Combined (L/100 km)"] < df["City (L/100 km)"])
            ).mean()
        ),
        "valid_fuel_type": float(df["Fuel type"].isin(["X","Z","D","E","N"]).mean()),
    }
    return {
        "overall_completeness": completeness,
        "rows_with_missing_values": int(df.isna().any(axis=1).sum()),
        "rule_scores": rules,
        "overall_quality_score": 10 * float(np.mean(list(rules.values()))),
    }

def quality_summary_table(results: dict) -> pd.DataFrame:
    rows = [
        {"metric": "overall_completeness", "value": results["overall_completeness"]},
        {"metric": "overall_quality_score_out_of_10", "value": results["overall_quality_score"]},
    ]
    rows.extend({"metric": k, "value": v} for k, v in results["rule_scores"].items())
    return pd.DataFrame(rows)
