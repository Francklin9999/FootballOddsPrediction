import pandas as pd
import numpy as np

weights = {
    "HomeAvgGoals": 0.4,
    "HomeAvgConceded": 0.3,
    "HomeGoalDiffAvg": 0.2,
    "HomeWinStreak": 0.1,
    "AwayAvgGoals": 0.4,
    "AwayAvgConceded": 0.3,
    "AwayGoalDiffAvg": 0.2,
    "AwayWinStreak": 0.1,
    "HomeLastMatch": 0.1,
    "AwayLastMatch": 0.1
}

def calculate_weighted_goals(data, weights):
    total_weight = sum(weights.values())
    weighted_goals = sum(data[key] * weights.get(key, 0) for key in data)
    return weighted_goals / total_weight

def simulate_match(home_avg_goals, away_avg_goals, num_simulations=10000):
    home_goals = np.random.poisson(home_avg_goals, num_simulations)
    away_goals = np.random.poisson(away_avg_goals, num_simulations)

    home_wins = np.sum(home_goals > away_goals)
    draws = np.sum(home_goals == away_goals)
    away_wins = np.sum(home_goals < away_goals)

    home_win_prob = home_wins / num_simulations
    draw_prob = draws / num_simulations
    away_win_prob = away_wins / num_simulations

    return home_win_prob, draw_prob, away_win_prob, home_goals, away_goals

def calculate_over_2_5_goals(home_goals, away_goals):
    total_goals = home_goals + away_goals
    over_2_5_goals = np.sum(total_goals > 2)
    return over_2_5_goals / len(total_goals)

def adjust_odds(market_home_win_odds, market_draw_odds, market_away_win_odds, home_win_prob, draw_prob, away_win_prob):
    market_home_win_odds = float(market_home_win_odds)
    market_draw_odds = float(market_draw_odds)
    market_away_win_odds = float(market_away_win_odds)
    home_win_prob = float(home_win_prob)
    draw_prob = float(draw_prob)
    away_win_prob = float(away_win_prob)

    home_win_prob_from_odds = 1 / market_home_win_odds
    draw_prob_from_odds = 1 / market_draw_odds
    away_win_prob_from_odds = 1 / market_away_win_odds

    total_prob = home_win_prob_from_odds + draw_prob_from_odds + away_win_prob_from_odds

    if total_prob > 1:
        home_win_prob_from_odds /= total_prob
        draw_prob_from_odds /= total_prob
        away_win_prob_from_odds /= total_prob

    adjusted_home_win_odds = market_home_win_odds * home_win_prob
    adjusted_draw_odds = market_draw_odds * draw_prob
    adjusted_away_win_odds = market_away_win_odds * away_win_prob

    return adjusted_home_win_odds, adjusted_draw_odds, adjusted_away_win_odds



def select_columns(data, columns):
    return data[columns]

def run_simulation(df, home_team_id, away_team_id, market_home_win_odds, market_draw_odds, market_away_win_odds, num_simulations=10000):
    selected_row_home = None
    selected_row_away = None
    selected_columns_home = ["HomeLastMatch", "HomeAvgGoals", "HomeAvgConceded", "HomeGoalDiff", "HomeGoalDiffAvg", "HomeWinStreak"]
    selected_columns_away = ["AwayLastMatch", "AwayAvgGoals", "AwayAvgConceded", "AwayGoalDiff", "AwayGoalDiffAvg", "AwayWinStreak"]
    
    selected_row = df[(df["HomeTeam"] == home_team_id) & (df["AwayTeam"] == away_team_id)]

    if selected_row.empty:
        selected_row_home = df[df["HomeTeam"] == home_team_id].iloc[::-1].head(1)
        selected_row_away = df[df["AwayTeam"] == away_team_id].iloc[::-1].head(1)
        home_data = select_columns(selected_row_home, selected_columns_home)
        away_data = select_columns(selected_row_away, selected_columns_away)
    else:
        home_data = select_columns(selected_row, selected_columns_home)
        away_data = select_columns(selected_row, selected_columns_away)

    home_avg_goals = calculate_weighted_goals(home_data, weights)
    away_avg_goals = calculate_weighted_goals(away_data, weights)

    home_win_prob, draw_prob, away_win_prob, home_goals, away_goals = simulate_match(home_avg_goals, away_avg_goals, num_simulations)

    over_2_5_prob = calculate_over_2_5_goals(home_goals, away_goals)

    adjusted_home_win_odds = 1 / home_win_prob 
    adjusted_draw_odds = 1 / draw_prob
    adjusted_away_win_odds = 1 / away_win_prob

    return round(home_win_prob, 2), round(draw_prob, 2), round(away_win_prob, 2), round(over_2_5_prob, 2), round(adjusted_home_win_odds, 2), round(adjusted_draw_odds, 2), round(adjusted_away_win_odds, 2)


if __name__ == "__main__":

    df = pd.read_csv("./data/clean/csv/cleaned_E0-2425.csv")

    home_team_id = 0
    away_team_id = 2

    market_home_win_odds = 2.0
    market_draw_odds = 3.5
    market_away_win_odds = 4.0

    results = run_simulation(
        df, home_team_id, away_team_id, weights, 
        market_home_win_odds, market_draw_odds, market_away_win_odds
    )

    print(f"Simulated Home Win Probability: {results['home_win_prob']:.2f}")
    print(f"Simulated Draw Probability: {results['draw_prob']:.2f}")
    print(f"Simulated Away Win Probability: {results['away_win_prob']:.2f}")
    print(f"Simulated Probability of Over 2.5 Goals: {results['over_2_5_prob']:.2f}")
    print(f"Adjusted Home Win Odds: {results['adjusted_home_win_odds']:.2f}")
    print(f"Adjusted Draw Odds: {results['adjusted_draw_odds']:.2f}")
    print(f"Adjusted Away Win Odds: {results['adjusted_away_win_odds']:.2f}")
