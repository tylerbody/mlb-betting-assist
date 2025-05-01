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
    total_used = 0.0

    if fixed_bet_amount and fixed_bet_count:
        stake = fixed_bet_amount
        for _ in range(fixed_bet_count):
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

    while total_used < bankroll:
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

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Multi-Sport Prop Bet Assistant V4", layout="wide")
st.title("Daily Prop Bet Assistant (MLB, NBA, NHL — Parlay Optimizer)")

tabs = st.tabs(["Smart Parlay Builder", "Custom Parlay Builder"])

# Tab 1: Smart Parlay Builder
tabs[0].subheader("Smart Mode: Let the system choose bet count and legs")
sport = tabs[0].selectbox("Select Sport", options=["MLB", "NBA", "NHL", "Mixed"], key="sport1")
bankroll = tabs[0].number_input("Enter your daily bankroll", min_value=10, max_value=1000, value=40, step=5, key="bankroll1")

if tabs[0].button("Generate Smart Bets"):
    parlays = simulate_parlays(bankroll, sport)
    for idx, parlay in enumerate(parlays):
        tabs[0].markdown(f"### Parlay {idx+1} — Stake: ${parlay['stake']}")
        for leg in parlay['legs']:
            tabs[0].markdown(f"- **{leg['Player']}** — {leg['Prop']} **{leg['Pick']} {leg['Line']}** (Confidence: {int(leg['Confidence']*100)}%)")

# Tab 2: Custom Parlay Builder
tabs[1].subheader("Custom Mode: You choose leg count and bet amount")
sport_custom = tabs[1].selectbox("Select Sport", options=["MLB", "NBA", "NHL", "Mixed"], key="sport2")
bet_amount = tabs[1].number_input("Amount per bet ($)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
bet_count = tabs[1].number_input("Number of bets", min_value=1, max_value=10, value=3, step=1)
legs_per_bet = tabs[1].number_input("Number of legs per bet", min_value=2, max_value=6, value=3, step=1)

if tabs[1].button("Generate Custom Bets"):
    parlays = simulate_parlays(bankroll=None, sport=sport_custom, fixed_legs=legs_per_bet, fixed_bet_amount=bet_amount, fixed_bet_count=bet_count)
    for idx, parlay in enumerate(parlays):
        tabs[1].markdown(f"### Parlay {idx+1} — Stake: ${parlay['stake']}")
        for leg in parlay['legs']:
            tabs[1].markdown(f"- **{leg['Player']}** — {leg['Prop']} **{leg['Pick']} {leg['Line']}** (Confidence: {int(leg['Confidence']*100)}%)")
