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

# -----------------------------
# Generate Fake Player Prop Data
# -----------------------------
def generate_fake_data():
    days = pd.date_range(end=datetime.date.today(), periods=7)
    values = np.random.normal(loc=5, scale=1.5, size=7)
    values = [max(0, round(v, 2)) for v in values]
    return pd.DataFrame({"Date": days, "Value": values})

# -----------------------------
# Simulate Optimized Parlay Bets
# -----------------------------
def simulate_parlays(bankroll, sport):
    props = SPORT_PROP_CATEGORIES[sport]
    players = SPORT_PLAYERS[sport]
    parlays = []
    total_used = 0.0

    while total_used < bankroll:
        remaining = bankroll - total_used
        max_stake = min(remaining, 15)
        min_stake = min(5, max_stake)
        stake = round(random.uniform(min_stake, max_stake), 2)
        num_legs = random.randint(2, 6)
        parlay = []
        for _ in range(num_legs):
            prop = random.choice(list(props.keys()))
            player = random.choice(players)
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
st.set_page_config(page_title="Multi-Sport Prop Bet Assistant V3", layout="wide")
st.title("Daily Prop Bet Assistant (MLB, NBA, NHL — Parlay Optimizer)")

sport = st.selectbox("Select Sport", options=["MLB", "NBA", "NHL"])
bankroll = st.number_input("Enter your daily bankroll", min_value=10, max_value=1000, value=40, step=5)

if st.button("Generate Today's Bet Slips"):
    parlays = simulate_parlays(bankroll, sport)
    st.subheader(f"Generated Multi-Leg Parlay Slips ({sport})")
    for idx, parlay in enumerate(parlays):
        st.markdown(f"### Parlay {idx+1} — Stake: ${parlay['stake']}")
        for leg in parlay['legs']:
            st.markdown(f"- **{leg['Player']}** — {leg['Prop']} **{leg['Pick']} {leg['Line']}** (Confidence: {int(leg['Confidence']*100)}%)")

    st.subheader("Performance Charts (Past 7 Games — Simulated)")
    for idx, parlay in enumerate(parlays):
        for leg in parlay['legs']:
            st.markdown(f"**{leg['Player']} — {leg['Prop']} ({leg['Pick']} {leg['Line']})**")
            data = generate_fake_data()
            bar_chart = alt.Chart(data).mark_bar().encode(
                x='Date:T',
                y='Value:Q',
                tooltip=['Date', 'Value']
            ).properties(height=200)
            rule = alt.Chart(pd.DataFrame({'y': [leg['Line']]})).mark_rule(color='red').encode(y='y')
            st.altair_chart(bar_chart + rule, use_container_width=True)

st.caption("This is a simulated prototype using fake data. Real player stats and odds integration coming next.")
