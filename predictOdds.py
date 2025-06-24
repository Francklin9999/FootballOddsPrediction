import pandas as pd
import joblib

win_model = joblib.load("./data/models/win_model.joblib")
over25_odds_model = joblib.load("./data/models/over25_odds_model.joblib")
over25_model = joblib.load("./data/models/over25_model.joblib")
home_odds_model = joblib.load("./data/models/home_odds_model.joblib")
away_odds_model = joblib.load("./data/models/away_odds_model.joblib")
scaler_win = joblib.load("./data/models/scaler_win.pkl")
scaler_over25 = joblib.load("./data/models/scaler_over25.pkl")
scaler_over25_odds = joblib.load("./data/models/scaler_over25_odds.pkl")
scaler_away_odds = joblib.load("./data/models/scaler_away_odds.pkl")
scaler_home_odds = joblib.load("./data/models/scaler_home_odds.pkl")

def predict(data):
    df = pd.DataFrame([data])

    X = df[[
        "HomeTeam", "AwayTeam", "HomeLastMatch", "AwayLastMatch", 
        "HomeAvgGoals", "AwayAvgGoals", "HomeWinStreak", "AwayWinStreak",
        "HomeAvgConceded", "AwayAvgConceded", "HomeGoalDiffAvg", "AwayGoalDiffAvg"
    ]]
    
    X_win_pred = scaler_win.transform(X)
    X_over25_pred = scaler_over25.transform(X)
    X_home_odds_pred = scaler_home_odds.transform(X)
    X_away_odds_pred = scaler_away_odds.transform(X)
    X_over25_odds_pred = scaler_over25_odds.transform(X)

    win_pred = round(float(win_model.predict(X_win_pred)))
    win_pred = data["HomeTeam"] if win_pred >= 1 else data["AwayTeam"] if win_pred <= -1 else "Draw"
    over25_odds_pred = round(float(over25_odds_model.predict(X_over25_odds_pred)), 2)
    over25_pred = round(float(over25_model.predict(X_over25_pred)))
    over25_pred = "Will probably not hit." if over25_pred <= 0 else "Will probably hit."
    home_odds_pred = round(float(home_odds_model.predict(X_home_odds_pred)), 2)
    away_odds_pred = round(float(away_odds_model.predict(X_away_odds_pred)), 2)

    return win_pred, over25_odds_pred, over25_pred, home_odds_pred, away_odds_pred

