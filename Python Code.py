#Python code created in VS code

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from collections import Counter
import json
import os

DATA_FILE = "mood_log.json"

MOODS = {1: "Very Low", 2: "Low", 3: "Neutral", 4: "Good", 5: "Great"}
EMOTIONS = ["Anxious", "Calm", "Sad", "Happy", "Stressed",
            "Energised", "Tired", "Motivated", "Overwhelmed", "Content"]


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_mood():
    print("\nMood (1=Very Low, 5=Great):", {k: v for k, v in MOODS.items()})
    score = input("Enter 1-5: ").strip()
    if score not in [str(k) for k in MOODS]:
        print("Invalid input."); return

    print("\nEmotions:", {i+1: e for i, e in enumerate(EMOTIONS)})
    picks = input("Enter numbers (comma-separated): ").split(",")
    emotions = [EMOTIONS[int(p.strip())-1] for p in picks if p.strip().isdigit()
                and 1 <= int(p.strip()) <= len(EMOTIONS)]

    note = input("Note (optional): ").strip()

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "score": int(score),
        "mood": MOODS[int(score)],
        "emotions": emotions,
        "note": note
    }
    data = load_data()
    data.append(entry)
    save_data(data)
    print(f"Logged: {entry['mood']} on {entry['date']}")


def summary():
    data = load_data()
    if not data:
        print("No entries found."); return
    df = pd.DataFrame(data)
    print(f"\nEntries      : {len(df)}")
    print(f"Average mood : {df['score'].mean():.2f}/5")
    print(f"Best day     : {df.loc[df['score'].idxmax(), 'date']} ({df['score'].max()}/5)")
    print(f"Worst day    : {df.loc[df['score'].idxmin(), 'date']} ({df['score'].min()}/5)")
    top = Counter(e for row in df["emotions"] for e in row).most_common(3)
    print(f
