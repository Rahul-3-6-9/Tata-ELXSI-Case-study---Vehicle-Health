from services.battery_health_service import BatteryHealthService, BatteryInput

def test_normal_case():
    service = BatteryHealthService()
    data = BatteryInput(soc=80, temperature=30, charge_cycles=500)
    result = service.process(data)

    assert 0 <= result.health_score <= 100
    assert result.risk_level in ["LOW", "MEDIUM", "HIGH"]

def test_high_temp_risk():
    service = BatteryHealthService()
    data = BatteryInput(soc=70, temperature=70, charge_cycles=300)
    result = service.process(data)

    assert result.risk_level == "HIGH"

def test_invalid_soc():
    service = BatteryHealthService()
    data = BatteryInput(soc=150, temperature=25, charge_cycles=200)

    try:
        service.process(data)
        assert False, "Expected ValueError for invalid SoC"
    except ValueError as e:
        assert str(e) == "Invalid SoC"

def test_invalid_temperature():
    service = BatteryHealthService()
    data = BatteryInput(soc=50, temperature=-30, charge_cycles=100)

    try:
        service.process(data)
        assert False, "Expected ValueError for invalid temperature"
    except ValueError as e:
        assert str(e) == "Invalid temperature"

def test_low_health_medium_risk():
    service = BatteryHealthService()
    data = BatteryInput(soc=40, temperature=25, charge_cycles=4000)
    result = service.process(data)

    assert result.risk_level == "MEDIUM"

