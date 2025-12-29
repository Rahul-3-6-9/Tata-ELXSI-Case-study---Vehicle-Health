import numpy as np
import pandas as pd

np.random.seed(42)

num_samples = 2000

soc = np.random.uniform(10, 100, num_samples)
temperature = np.random.uniform(20, 70, num_samples)
charge_cycles = np.random.randint(0, 3000, num_samples)

# Simple physics-inspired degradation logic
health_score = (
    100
    - 0.01 * charge_cycles
    - 0.3 * np.maximum(temperature - 30, 0)
    - 0.1 * np.maximum(50 - soc, 0)
)

# Clamp between 0 and 100
health_score = np.clip(health_score, 0, 100)

df = pd.DataFrame({
    "soc": soc,
    "temperature": temperature,
    "charge_cycles": charge_cycles,
    "health_score": health_score
})

df.to_csv(r"C:\Users\rahul\Downloads\Data Analysis\TATA_ELXSI_CS2\data\battery_data.csv", index=False)
print("battery_data.csv generated")
