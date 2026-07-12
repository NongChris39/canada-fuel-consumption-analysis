from src.feature_engineering import (
    infer_drivetrain, extract_speed_number,
    extract_transmission_type, simplify_vehicle_class,
)

def test_infer_drivetrain():
    assert infer_drivetrain("Model AWD") == "AWD"
    assert infer_drivetrain("Model 4WD") == "4WD / 4x4"
    assert infer_drivetrain("Model") == "Unknown / Other"

def test_transmission_parsing():
    assert extract_transmission_type("AS8") == "Automatic with select shift"
    assert extract_speed_number("AS8") == 8

def test_vehicle_class():
    assert simplify_vehicle_class("SUV: Small") == "SUV"
    assert simplify_vehicle_class("Pickup truck") == "Truck"
