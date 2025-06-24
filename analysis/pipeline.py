import pandas as pd
import os
import json

def read_csv(file_path):
    return pd.read_csv(file_path)

def preprocess_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values(by=["HomeTeam", "Date"])
    
    df["HomeLastMatch"] = df.groupby("HomeTeam")["Date"].diff().dt.days.fillna(7)
    df["AwayLastMatch"] = df.apply(
        lambda row: (row["Date"] - df[(df["AwayTeam"] == row["AwayTeam"]) & 
                                        (df["Date"] < row["Date"])]
                     ["Date"].max()).days
        if not df[(df["AwayTeam"] == row["AwayTeam"]) & (df["Date"] < row["Date"])].empty else 7, axis=1)
    
    df["HomeGoalDiff"] = df["FTHG"] - df["FTAG"]
    df["AwayGoalDiff"] = -df["HomeGoalDiff"]
    
    df["HomeAvgGoals"] = df.groupby("HomeTeam")["FTHG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df["AwayAvgGoals"] = df.groupby("AwayTeam")["FTAG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    
    df["HomeWinStreak"] = df.groupby("HomeTeam")["FTR"].transform(lambda x: x.eq("H").rolling(5, min_periods=1).sum())
    df["AwayWinStreak"] = df.groupby("AwayTeam")["FTR"].transform(lambda x: x.eq("A").rolling(5, min_periods=1).sum())
    
    df["HomeAvgConceded"] = df.groupby("HomeTeam")["FTAG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df["AwayAvgConceded"] = df.groupby("AwayTeam")["FTHG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    
    df["HomeGoalDiffAvg"] = df.groupby("HomeTeam")["HomeGoalDiff"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df["AwayGoalDiffAvg"] = df.groupby("AwayTeam")["AwayGoalDiff"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    
    return df

def preprocess_data_all(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df = df.sort_values(by=["HomeTeam", "Date"])
    
    df["HomeLastMatch"] = df.groupby("HomeTeam")["Date"].diff().dt.days.fillna(7)
    df["AwayLastMatch"] = df.apply(
        lambda row: (row["Date"] - df[(df["AwayTeam"] == row["AwayTeam"]) & 
                                        (df["Date"] < row["Date"])]
                     ["Date"].max()).days
        if not df[(df["AwayTeam"] == row["AwayTeam"]) & (df["Date"] < row["Date"])].empty else 7, axis=1)
    
    df["HomeGoalDiff"] = df["FTHG"] - df["FTAG"]
    df["AwayGoalDiff"] = -df["HomeGoalDiff"]
    
    df["HomeAvgGoals"] = df.groupby("HomeTeam")["FTHG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df["AwayAvgGoals"] = df.groupby("AwayTeam")["FTAG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    
    df["HomeWinStreak"] = df.groupby("HomeTeam")["FTR"].transform(lambda x: x.eq("H").rolling(5, min_periods=1).sum())
    df["AwayWinStreak"] = df.groupby("AwayTeam")["FTR"].transform(lambda x: x.eq("A").rolling(5, min_periods=1).sum())
    
    df["HomeAvgConceded"] = df.groupby("HomeTeam")["FTAG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df["AwayAvgConceded"] = df.groupby("AwayTeam")["FTHG"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    
    df["HomeGoalDiffAvg"] = df.groupby("HomeTeam")["HomeGoalDiff"].transform(lambda x: x.rolling(5, min_periods=1).mean())
    df["AwayGoalDiffAvg"] = df.groupby("AwayTeam")["AwayGoalDiff"].transform(lambda x: x.rolling(5, min_periods=1).mean())

    team_mapping = {team: idx for idx, team in enumerate(df["HomeTeam"].unique())}
    
    return df, team_mapping

def clean_and_map_data(df):
    columns_to_keep = [
        "Date", "HomeTeam", "AwayTeam", "HomeLastMatch", "AwayLastMatch", "HomeGoalDiff", "AwayGoalDiff",
        "HomeAvgGoals", "AwayAvgGoals", "HomeWinStreak", "AwayWinStreak", "HomeAvgConceded", "AwayAvgConceded",
        "HomeGoalDiffAvg", "AwayGoalDiffAvg", "FTHG", "FTAG", "FTR", "AvgH", "AvgD", "AvgA", "Avg>2.5", "Avg<2.5"
    ]
    df = df[columns_to_keep]
    
    rename_map = {
        "FTHG": "FullTimeHomeTeamGoals",
        "FTAG": "FullTimeAwayTeamGoals",
        "FTR": "FullTimeResult",
        "AvgH": "MarketAverageHomeWinOdds",
        "AvgD": "MarketAverageDrawWinOdds",
        "AvgA": "MarketAverageAwayWinOdds",
        "Avg>2.5": "MarketAverageOver2.5Goals",
        "Avg<2.5": "MarketAverageUnder2.5Goals"
    }
    df = df.rename(columns=rename_map)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir, "..", "data", "clean", "json", "team_mapping_E0.json")

    team_mapping = json.load(open(file_path))
    
    df["HomeTeam"] = df["HomeTeam"].map(team_mapping)
    df["AwayTeam"] = df["AwayTeam"].map(team_mapping)
    df["FullTimeResult"] = df["FullTimeResult"].map({"H": 1, "D": 0, "A": -1})
    
    df = df.drop(columns=["Date"])
    df = df.round({col: 2 for col in df.select_dtypes(include=['float']).columns})
    df[["HomeLastMatch", "HomeWinStreak", "AwayWinStreak"]] = df[["HomeLastMatch", "HomeWinStreak", "AwayWinStreak"]].astype(int)
    
    return df

def save_to_csv(df, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)

def transform_data(input_file):
    project_root = os.path.abspath(os.path.dirname(__file__))

    output_file_csv = os.path.join(project_root, 'data', 'clean', 'csv', f"cleaned_{os.path.basename(input_file)}")
    
    df = read_csv(input_file)
    df = preprocess_data(df)
    df = clean_and_map_data(df)
    save_to_csv(df, output_file_csv)
    
    return df

def transform_data_all(input_file):
    project_root = os.path.abspath(os.path.dirname(__file__))

    output_file_csv = os.path.join(project_root, 'data', 'clean', 'csv', f"cleaned_{os.path.basename(input_file)}")
    
    df = read_csv(input_file)
    df, json_data = preprocess_data_all(df)
    df = clean_and_map_data(df)
    save_to_csv(df, output_file_csv)
    
    return df, json_data


if __name__ == "__main__":
    input_file = "../data/sample/E0-2021.csv"
    df = transform_data(input_file)
    print("Processing complete")
