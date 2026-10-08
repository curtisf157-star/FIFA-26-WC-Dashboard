import os
import numpy as np
import pandas as pd

os.makedirs("cleaned", exist_ok=True)

def clean_columns(df):
    df.columns = (
        df.columns.astype(str).str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
    )
    return df

def clean_text(df):
    for col in df.columns:
        if df[col].dtype == object or str(df[col].dtype) == "str":
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": None, "None": None, "": None})
    return df

def to_int(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    return df

def to_float(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def to_date(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def save(df, filename):
    df.to_csv("cleaned/" + filename, index=False)
    print(f"[OK] {filename:32s} -> {df.shape}")

def load(name):
    df = pd.read_csv(name, low_memory=False)
    return clean_text(clean_columns(df))

# 1. TEAMS
teams = load("teams.csv").drop_duplicates(subset=["team_id"])
teams = to_int(teams, ["team_id", "fifa_ranking_pre_tournament"])
teams = to_float(teams, ["elo_rating"])
save(teams, "teams_clean.csv")

# 2. VENUES
venues = load("venues.csv").drop_duplicates(subset=["venue_id"])
venues = to_int(venues, ["venue_id", "capacity", "elevation_meters"])
venues = to_float(venues, ["latitude", "longitude"])
save(venues, "venues_clean.csv")

# 3. REFEREES
referees = load("referees.csv").drop_duplicates(subset=["referee_id"])
referees = to_int(referees, ["referee_id"])
referees = to_float(referees, ["avg_cards_per_game"])
save(referees, "referees_clean.csv")

# 4. TOURNAMENT STAGES
stages = load("tournament_stages.csv").drop_duplicates(subset=["stage_id"])
stages = to_int(stages, ["stage_id", "is_knockout"])
save(stages, "tournament_stages_clean.csv")

# 5. MATCHES
matches = load("matches.csv").drop_duplicates(subset=["match_id"])
matches = to_int(matches, [
    "match_id", "stage_id", "venue_id", "home_team_id", "away_team_id",
    "home_score", "away_score", "home_penalty_score", "away_penalty_score",
    "referee_id", "player_of_the_match_id",
])
matches = to_float(matches, ["home_xg", "away_xg"])
matches = to_date(matches, ["date"])
matches["total_goals"] = matches["home_score"] + matches["away_score"]
matches["goal_difference"] = matches["home_score"] - matches["away_score"]
matches["is_draw"] = (matches["home_score"] == matches["away_score"]).astype(int)
matches["match_outcome"] = np.where(
    matches["home_score"] > matches["away_score"], "Home Win",
    np.where(matches["home_score"] < matches["away_score"], "Away Win", "Draw"),
)
save(matches, "matches_clean.csv")

# 6. MATCHES DETAILED
md = load("matches_detailed.csv").drop_duplicates(subset=["match_id"])
md = to_int(md, ["match_id", "home_score", "away_score",
                 "home_penalty_score", "away_penalty_score"])
md = to_float(md, ["home_xg", "away_xg"])
md = to_date(md, ["date"])
md["total_goals"] = md["home_score"] + md["away_score"]
save(md, "matches_detailed_clean.csv")

# 7. PLAYERS
players = load("squads_and_players.csv").drop_duplicates(subset=["player_id"])
players = to_int(players, ["player_id", "team_id", "caps", "height_cm", "goals"])
players = to_float(players, ["market_value_eur"])
players = to_date(players, ["date_of_birth"])
players["age"] = ((pd.Timestamp("2026-06-01") - players["date_of_birth"]).dt.days / 365.25).round(1)
save(players, "players_clean.csv")

# 8. PLAYER STATS
ps = load("player_stats.csv").drop_duplicates(subset=["player_id"])
ps = to_int(ps, [
    "player_id", "team_id", "matches_played", "matches_started",
    "minutes_played", "goals", "assists", "shots", "shots_on_target",
    "yellow_cards", "red_cards", "penalty_goals", "own_goals",
    "clean_sheets", "saves", "goals_conceded",
])
ps = to_float(ps, ["average_rating"])
ps["goal_contributions"] = ps["goals"] + ps["assists"]
ps["goals_per_90"] = (ps["goals"] * 90 / ps["minutes_played"].replace(0, np.nan)).round(2)
ps["assists_per_90"] = (ps["assists"] * 90 / ps["minutes_played"].replace(0, np.nan)).round(2)
ps["shot_accuracy_pct"] = (ps["shots_on_target"] / ps["shots"].replace(0, np.nan) * 100).round(1)
save(ps, "player_stats_clean.csv")

# 9. MATCH TEAM STATS
mts = load("match_team_stats.csv")
mts = to_int(mts, ["match_id", "team_id", "possession_pct", "total_shots",
                   "shots_on_target", "corners", "fouls", "offsides", "saves"])
mts = to_date(mts, ["last_updated"])
mts["shot_accuracy_pct"] = (mts["shots_on_target"] / mts["total_shots"].replace(0, np.nan) * 100).round(1)
save(mts, "match_team_stats_clean.csv")

# 10. MATCH EVENTS
ev = load("match_events.csv").drop_duplicates(subset=["event_id"])
ev = to_int(ev, ["event_id", "match_id", "minute", "team_id", "player_id"])
save(ev, "match_events_clean.csv")

# 11. MATCH LINEUPS
lu = load("match_lineups.csv").drop_duplicates(subset=["lineup_id"])
lu = to_int(lu, ["lineup_id", "match_id", "player_id", "team_id",
                 "is_starting_xi", "minutes_played"])
save(lu, "match_lineups_clean.csv")

print("\nDone. Look for the cleaned folder.")