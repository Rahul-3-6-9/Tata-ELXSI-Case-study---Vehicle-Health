import joblib
import numpy as np
from pydantic import BaseModel

class BatteryInput(BaseModel):
    soc: float
    temperature: float
    charge_cycles: int

class BatteryOutput(BaseModel):
    health_score: float
    risk_level: str
    explanation: str

class BatteryHealthService:

    def __init__(self):
        self.model = joblib.load("models/battery_model.pkl")

    def validate(self, data: BatteryInput):
        if not 0 <= data.soc <= 100:
            raise ValueError("Invalid SoC")
        if not -20 <= data.temperature <= 80:
            raise ValueError("Invalid temperature")

    def process(self, data: BatteryInput) -> BatteryOutput:
        self.validate(data)

        features = np.array([[data.soc, data.temperature, data.charge_cycles]])
        health = float(self.model.predict(features)[0])

        explanation_parts = []

        # SAFETY RULES (ordered by priority)

        if data.temperature > 60:
            risk = "HIGH"
            explanation_parts.append(
                f"Critical battery temperature detected ({data.temperature}°C > 60°C)"
            )

        elif data.charge_cycles > 4500:
            risk = "HIGH"
            explanation_parts.append(
                f"Battery has exceeded safe aging limit ({data.charge_cycles} charge cycles)"
            )

        elif data.charge_cycles > 3000:
            risk = "MEDIUM"
            explanation_parts.append(
                f"Battery shows advanced aging ({data.charge_cycles} charge cycles)"
            )

        elif health < 60:
            risk = "MEDIUM"
            explanation_parts.append(
                f"Predicted battery health is reduced ({round(health, 2)} < 60)"
            )

        else:
            risk = "LOW"
            explanation_parts.append(
                "Battery operating within normal temperature, aging, and health limits"
            )



        explanation = "; ".join(explanation_parts)

        return BatteryOutput(
            health_score=round(health, 2),
            risk_level=risk,
            explanation=explanation
        )
