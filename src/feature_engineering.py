import re
import pandas as pd
from .config import COLUMNS_TO_DROP

COUNTRY_BY_MAKE = {
    "Ford":"United States","Chevrolet":"United States","GMC":"United States",
    "Jeep":"United States","Dodge":"United States","Cadillac":"United States",
    "Ram":"United States","Buick":"United States","Lincoln":"United States",
    "Chrysler":"United States","Tesla":"United States",
    "BMW":"Germany","Mercedes-Benz":"Germany","Porsche":"Germany","Audi":"Germany",
    "Volkswagen":"Germany","smart":"Germany","Bugatti":"Germany",
    "Toyota":"Japan","Nissan":"Japan","Honda":"Japan","Mazda":"Japan",
    "Subaru":"Japan","Mitsubishi":"Japan","Lexus":"Japan","Infiniti":"Japan",
    "Acura":"Japan","Scion":"Japan",
    "Hyundai":"South Korea","Kia":"South Korea","Genesis":"South Korea",
    "Jaguar":"United Kingdom","Land Rover":"United Kingdom","MINI":"United Kingdom",
    "Bentley":"United Kingdom","Rolls-Royce":"United Kingdom",
    "Aston Martin":"United Kingdom",
    "FIAT":"Italy","Maserati":"Italy","Alfa Romeo":"Italy",
    "Ferrari":"Italy","Lamborghini":"Italy","Volvo":"Sweden",
}

TRANSMISSION_NAMES = {
    "M":"Manual","A":"Automatic","AM":"Automated manual",
    "AS":"Automatic with select shift","AV":"Continuously variable",
}

def infer_drivetrain(model_name) -> str:
    text = str(model_name).upper()
    if re.search(r"\b(4WD|4X4)\b", text): return "4WD / 4x4"
    if re.search(r"\bAWD\b", text): return "AWD"
    if re.search(r"\bFWD\b", text): return "FWD"
    if re.search(r"\bRWD\b", text): return "RWD"
    return "Unknown / Other"

def infer_flexible_fuel(model_name) -> bool:
    text = str(model_name).upper()
    return any(x in text for x in ("FFV","FLEX FUEL","E85"))

def simplify_vehicle_class(name) -> str:
    """Map a detailed vehicle class to a broader category."""

    text = str(name).strip().lower()

    if (
        "sport utility vehicle" in text
        or text.startswith("suv")
        or " suv" in text
    ):
        return "SUV"

    if (
        "pickup truck" in text
        or text.startswith("truck")
    ):
        return "Truck"

    if any(
        category in text
        for category in (
            "compact",
            "subcompact",
            "minicompact",
        )
    ):
        return "Compact"

    if "station wagon" in text:
        return "Station wagon"

    if (
        "two-seater" in text
        or "two seater" in text
    ):
        return "Two-seater"

    if (
        "van" in text
        or "minivan" in text
    ):
        return "Van"

    return "Other"

def extract_transmission_type(value) -> str:
    code = "".join(c for c in str(value).upper() if c.isalpha())
    return TRANSMISSION_NAMES.get(code, "Unknown")

def extract_speed_number(value):
    digits = "".join(c for c in str(value) if c.isdigit())
    return int(digits) if digits else pd.NA

def clean_and_engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result = result.drop(columns=[c for c in COLUMNS_TO_DROP if c in result], errors="ignore")
    required = [
        "Model year","Make","Model","Vehicle class","Engine size (L)","Cylinders",
        "Transmission","Fuel type","City (L/100 km)","Highway (L/100 km)",
        "Combined (L/100 km)",
    ]
    result = result.dropna(subset=required).copy()
    result["Manufacturer country"] = result["Make"].map(COUNTRY_BY_MAKE).fillna("Unknown")
    result["Drivetrain inferred"] = result["Model"].apply(infer_drivetrain)
    result["Flexible fuel inferred"] = result["Model"].apply(infer_flexible_fuel)
    result["Vehicle class simplified"] = result["Vehicle class"].apply(simplify_vehicle_class)
    result["Transmission type"] = result["Transmission"].apply(extract_transmission_type)
    result["Speed count"] = result["Transmission"].apply(extract_speed_number).astype("Int64")
    return result
