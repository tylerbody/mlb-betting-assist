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
    "MLB": {
        "Hitter Fantasy Score": "hitter",
        "Total Bases": "hitter",
        "Pitcher Strikeouts": "pitcher",
        "1st Inning Runs Allowed": "pitcher",
        "Hits + Runs + RBIs": "hitter",
        "Home Runs": "hitter",
        "Pitcher Fantasy Score": "pitcher",
        "Hits Allowed": "pitcher",
        "Stolen Bases": "hitter",
        "Doubles": "hitter",
        "Walks Allowed": "pitcher",
        "1st Inning Walks Allowed": "pitcher",
        "Singles": "hitter",
        "Pitching Outs": "pitcher",
        "Walks": "hitter",
        "Hits": "hitter",
        "Earned Runs Allowed": "pitcher",
        "RBIs": "hitter",
        "Runs": "hitter",
        "Hitter Strikeouts": "hitter"
    },
    "NBA": {
        "Assists": "player",
        "Points + Rebounds + Assists": "player",
        "Points": "player",
        "Rebounds": "player",
        "3-PT Made": "player",
        "Points + Assists": "player",
        "FG Made": "player",
        "Points in First 5 Minutes": "player",
        "Defensive Rebounds": "player",
        "PRA in First 5 Minutes": "player",
        "Fantasy Score": "player",
        "Rebounds + Assists": "player",
        "Offensive Rebounds": "player",
        "3-PT Attempted": "player",
        "Free Throws Made": "player",
        "FG Attempted": "player",
        "Points + Rebounds": "player",
        "Dunks": "player",
        "Blocked Shots": "player",
        "Steals": "player",
        "Personal Fouls": "player",
        "Free Throws Attempted": "player",
        "Turnovers": "player",
        "Two Pointers Attempted": "player",
        "Two Pointers Made": "player"
    },
    "NHL": {
        "Assists": "player",
        "Goalie Saves": "goalie",
        "Points": "player",
        "Goals": "player",
        "Shots on Goal": "player",
        "Time on Ice": "player",
        "Faceoffs Won": "player",
        "Hits": "player",
        "Blocked Shots": "player"
    }
}

SPORT_PLAYERS = {
    "MLB": ["Mookie Betts", "Spencer Strider", "Aaron Judge", "Freddie Freeman", "Ronald Acuna Jr."],
    "NBA": ["LeBron James", "Stephen Curry", "Luka Doncic", "Jayson Tatum", "Nikola Jokic"],
    "NHL": ["Connor McDavid", "Sidney Crosby", "Auston Matthews", "Alex Ovechkin", "Igor Shesterkin"]
}

def generate_fake_data():
    days = pd.date_range(end=datetime.date.today(), periods=7)
    values = np.random.normal(loc=5, scale=1.5, size=7)
    values = [max(0, round(v, 2)) for v in values]
    return pd.DataFrame({"Date": days, "Value": values})

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
            stake = max(5, fixed_bet_amount)  # Enforce $5 minimum stake
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
        min_stake = max(5, min(5, max_stake))  # Enforce $5 minimum stake
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
