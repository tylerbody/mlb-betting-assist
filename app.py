import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime
import altair as alt

# -----------------------------
# Prop Categories by Sport
# -----------------------------
SPORT_PROP_CATEGORIES = {
    "MLB": { ... },  # same as before
    "NBA": { ... },  # same as before
    "NHL": { ... }   # same as before
}

SPORT_PLAYERS = { ... }  # same as before

# -----------------------------
# Generate Fake Player Prop Data
# -----------------------------
def generate_fake_data():
    days = pd.date_range(end=datetime.date.today(), periods=7)
    values = np.random.normal(loc=5, scale=1.5, size=7)
    values = [max(0, round(v, 2)) for v in values]
    return pd.DataFrame({"Date": days, "Value": values})

# -----------------------------
# Simulate Parlay Bets with Optional Custom Settings
# -----------------------------
def simulate_parlays(bankroll, sport, fixed_legs=None, fixed_bet_amount=None, fixed_bet_count=None):
    if sport == "Mixed":
        combined_props = {k: v for d in SPORT_PROP_CATEGORIES.values() for k, v in d.items()}
        combined_players = sum(SPORT_PLAYERS.values(), [])
    else:
        combined_props = SPORT_PROP_CATEGORIES[sport]
        combined_players = SPORT_PLAYERS[sport]

    parlays = []

    if fixed_bet_amount is not None and fixed_bet_count is not None:
        for _ in range(fixed_bet_count):
            stake = fixed_bet_amount
            num_legs = fixed_legs or random.randint(2, 6)
            parlay = []
            for _ in range(num_legs):
                prop = random.choice(list(combined_props.keys()))
                player = random.choice(combined_players)
                line = round(random.uniform(0.5, 3.0), 1)
                pick = random.choice(["Over", "Under"])
                confidence = round(random.uniform(0.7, 0.95), 2)
                parlay.append({
                    "Player": player,
                    "Prop": prop,
                    "Line": line,
                    "Pick": pick,
                    "Confidence": confidence
                })
            parlays.append({"stake": stake, "legs": parlay})
        return parlays

    total_used = 0.0
    while bankroll is not None and total_used < bankroll:
        remaining = bankroll - total_used
        max_stake = min(remaining, 15)
        min_stake = min(5, max_stake)
        stake = round(random.uniform(min_stake, max_stake), 2)
        num_legs = random.randint(2, 6)
        parlay = []
        for _ in range(num_legs):
            prop = random.choice(list(combined_props.keys()))
            player = random.choice(combined_players)
            line = round(random.uniform(0.5, 3.0), 1)
            pick = random.choice(["Over", "Under"])
            confidence = round(random.uniform(0.7, 0.95), 2)
            parlay.append({
                "Player": player,
                "Prop": prop,
                "Line": line,
                "Pick": pick,
                "Confidence": confidence
            })
        parlays.append({"stake": stake, "legs": parlay})
        total_used = round(total_used + stake, 2)

    return parlays
