from fastapi import FastAPI
from services.battery_health_service import (
    BatteryHealthService,
    BatteryInput
)

app = FastAPI(title="SDV Vehicle Health API")

battery_service = BatteryHealthService()

@app.post("/battery/health")
def battery_health(data: BatteryInput):
    return battery_service.process(data)
