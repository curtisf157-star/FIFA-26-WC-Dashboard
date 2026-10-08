# FIFA 2026 World Cup — Interactive Power BI Dashboard

![Dashboard Overview](images/01-overview.png)

## 📌 Project Overview
This end-to-end data analytics project explores the FIFA 2026 World Cup. It covers the complete data pipeline: extracting raw CSV data, cleaning and transforming it using Python (pandas), building a relational data model in Power BI, authoring DAX measures, and designing a 5-page interactive dashboard. 

The goal of this project is to demonstrate the ability to turn raw data into actionable insights for a tournament comprising 104 matches, 48 teams, and 1,248 players.

## 🎯 Objectives
- Clean and standardise 14 raw tournament datasets into 11 analysis-ready files.
- Design a star schema data model to support fast, interactive filtering.
- Author DAX measures for advanced tournament and player metrics.
- Build a multi-page interactive Power BI dashboard for tournament analysis.
- Showcase a professional end-to-end data portfolio project.

## 📊 Key Findings
- **Tournament Scale:** 104 matches played, producing 308 total goals (2.96 goals per match).
- **Top Scorer:** Kylian Mbappé leads the tournament with 8 goals.
- **Match Outcomes:** Home wins (48%), Draws (28.85%), Away wins (23.08%).
- **Discipline:** 35 yellow cards and 12 red cards issued across the tournament.

## 🛠️ Tools & Technologies
- **Data Cleaning & Prep:** Python 3.13, pandas, NumPy
- **Data Modelling & Visualisation:** Microsoft Power BI Desktop
- **Query Language:** Power Query (M), DAX (Data Analysis Expressions)
- **Version Control:** Git, GitHub

## 📂 Dataset
The raw dataset consists of 14 CSV files covering:
- `matches.csv` & `matches_detailed.csv`: Match results, xG, and stadium details.
- `teams.csv`, `players.csv`, `squads_and_players.csv`: Team and player dimensions.
- `player_stats.csv`, `match_team_stats.csv`: Fact tables for per-player and per-team match statistics.
- `match_events.csv`, `match_lineups.csv`: Event-level and lineup data.
- `venues.csv`, `referees.csv`, `tournament_stages.csv`: Supporting dimensions.

## 🧹 Data Preparation (Python)
The `clean_fifa_2026.py` script automates the cleaning process. Key steps include:
- Standardising column names to `snake_case`.
- Handling missing values and stripping whitespace.
- Enforcing correct data types (e.g., dates, integers, floats).
- Removing duplicates based on primary keys.
- **Feature Engineering:** Creating new calculated fields such as `total_goals`, `goal_difference`, `match_outcome`, `goals_per_90`, `assists_per_90`, and `shot_accuracy_pct`.

The script outputs 11 cleaned CSV files into the `cleaned/` folder.

## 🗄️ Data Model (Power BI)
A **Star Schema** was implemented to ensure optimal performance and accurate filtering:
- **Fact Tables:** `matches`, `player_stats`, `match_team_stats`, `match_events`, `match_lineups`
- **Dimension Tables:** `teams`, `players`, `venues`, `referees`, `tournament_stages`, `Date`
- **Relationships:** One-to-many relationships established between dimensions and fact tables (e.g., `teams[team_id]` → `matches[home_team_id]`).
- **Date Table:** A dedicated calendar table was created to enable time-intelligence analysis (goals over time).

## 📈 Dashboard Pages

### 1. Tournament Overview
**![Overview Page](images/01-overview.png)**
- **KPIs:** Total Matches, Total Goals, Total Teams, Total Players, Goals per Match.
- **Visuals:** Bar chart of Goals by Team, Line chart of Goals over Time, and a full Match Results table.

### 2. Team Analysis
**![Team Analysis Page](images/02-team-analysis.png)**
- **Interactivity:** Team slicer (dropdown).
- **Visuals:** Donut chart of Match Outcomes (Win/Draw/Loss), Bar chart of Top Scorers for the selected team, and a detailed Match Statistics table (Possession, Shots, Corners, Fouls).

### 3. Player Analysis
**![Player Analysis Page](images/03-player-analysis.png)**
- **Interactivity:** Player slicer (dropdown).
- **KPIs:** Selected Assists, Selected Minutes, Selected Goals, Selected Goals per 90, Selected Avg Rating.
- **Visuals:** Scatter plot of Minutes vs Goals (sized by Average Rating), Bar chart of Top 15 Tournament Scorers, and a comprehensive Player Performance table.

### 4. Player Comparison
**![Player Comparison Page](images/04-player-comparison.png)**
- **Interactivity:** Two independent player slicers (Player A and Player B).
- **Visuals:** Side-by-side KPI cards comparing Goals, Assists, Minutes, and Avg Rating. Includes a Top 15 Scorers chart and a comparative stats table.

### 5. Tournament Trends
**![Tournament Trends Page](images/05-tournament-trends.png)**
- **KPIs:** Goals per 90, Total Yellow Cards, Total Red Cards.
- **Visuals:** Line chart of Goals over Time, Bar chart of Goals by Tournament Stage, Bar chart of Total Cards by Team, and a Line chart of Cards over Time.

## 🧮 Key DAX Measures
Below are examples of the DAX measures created for this dashboard:

```dax
Total Matches = COUNTROWS(matches)

Total Goals = SUM(matches[total_goals])

Goals per Match = DIVIDE([Total Goals], [Total Matches])

Total Teams = DISTINCTCOUNT(teams[team_id])

Player Goals = SUM(player_stats[goals])

Goals per 90 = DIVIDE([Player Goals] * 90, [Total Minutes])

Avg Rating = AVERAGE(player_stats[average_rating])

Cards per Team = SUM(player_stats[yellow_cards]) + SUM(player_stats[red_cards])