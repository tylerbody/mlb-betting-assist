import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime
import altair as alt

# -----------------------------
# Sample Player Props and Categories
# -----------------------------
PROP_CATEGORIES = {
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
}

# -----------------------------
# Generate Fake Player Prop Data
# -----------------------------
def generate_fake_data(prop_type):
    days = pd.date_range(end=datetime.date.today(), periods=7)
    values = np.random.normal(loc=5 if "pitcher" in prop_type else 3, scale=1.5, size=7)
    values = [max(0, round(v, 2)) for v in values]
    return pd.DataFrame({"Date": days, "Value": values})

# -----------------------------
# Simulate Optimized Bets
# -----------------------------
def simulate_optimized_bets(bankroll):
    num_bets = random.randint(5, 10)
    bets = []
    for _ in range(num_bets):
        stake = round(bankroll / num_bets, 2)
        prop = random.choice(list(PROP_CATEGORIES.keys()))
        player = random.choice(["Aaron Judge", "Shohei Ohtani", "Spencer Strider", "Ronald Acuna Jr.", "Mookie Betts"])
        line = round(random.uniform(1.5, 6.0), 1)
        odds = random.choice(["+120", "-110", "+150", "-105"])
        confidence = round(random.uniform(0.65, 0.9), 2)
        bets.append({
            "Player": player,
            "Prop": prop,
            "Line": line,
            "Odds": odds,
            "Confidence": confidence,
            "Stake": stake
        })
    return bets

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="MLB Prop Bet Assistant", layout="wide")
st.title("MLB Daily Prop Bet Assistant (Prototype)")

bankroll = st.number_input("Enter your daily bankroll (e.g. $50)", min_value=10, max_value=1000, value=50, step=5)

if st.button("Generate Today's Bets"):
    bets = simulate_optimized_bets(bankroll)
    st.subheader("Suggested Bets")
    df = pd.DataFrame(bets)
    st.dataframe(df, use_container_width=True)

    # Plot last 7-day data for each prop
    st.subheader("Recent Player Performance (Past 7 Games)")
    for bet in bets:
        st.markdown(f"**{bet['Player']} — {bet['Prop']}**")
        data = generate_fake_data(PROP_CATEGORIES[bet['Prop']])
        chart = alt.Chart(data).mark_line(point=True).encode(
            x='Date:T',
            y='Value:Q',
            tooltip=['Date', 'Value']
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("Email Preview")
    email_preview = ""
    for bet in bets:
        email_preview += f"{bet['Player']} | {bet['Prop']} o/u {bet['Line']} | Odds: {bet['Odds']} | Stake: ${bet['Stake']} | Confidence: {int(bet['Confidence']*100)}%\n"
    st.text_area("Daily Picks Email Format", value=email_preview, height=300)
    st.success("Feature: Actual email delivery coming in v2.")

st.caption("This is a test version using simulated data. Real player stats and odds will be integrated in the next version.")
