import os
import time
import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = "data/events"
TMP_DIR = "data/tmp"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

print("Event generator started...")

while True:
    events = []

    for _ in range(10):
        events.append({
            "event_id": fake.uuid4(),
            "user_id": fake.random_int(1, 100),
            "event_type": fake.random_element(["view", "purchase"]),
            "product_id": fake.random_int(1, 50),
            "product_name": fake.word(),
            "price": round(fake.random_number(digits=2), 2),
            "event_timestamp": fake.date_time().isoformat()
        })

    df = pd.DataFrame(events)

    ts = int(time.time())
    tmp_file = f"{TMP_DIR}/events_{ts}.csv.tmp"
    final_file = f"{OUTPUT_DIR}/events_{ts}.csv"

    # Write to temp file first
    df.to_csv(tmp_file, index=False)

    # Atomic rename (Spark-safe)
    os.rename(tmp_file, final_file)

    print(f"Written file: {final_file}")

    time.sleep(3)
