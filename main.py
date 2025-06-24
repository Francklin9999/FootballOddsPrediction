from flask import Flask
from flask import Flask, request, jsonify
import json
import os
from simulation import run_simulation as simulation
from functions import *
from analysis.pipeline import transform_data, transform_data_all
from strategies import process_strategie, process_strategie_all
from predictOdds import predict


app = Flask(__name__)

team_mapping = json.load(open("./data/clean/json/team_mapping_E0.json"))
project_root = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
    return "/"

@app.route('/process_csv', methods=['POST'])
def process_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        input_file_path = os.path.join(project_root, 'data', 'uploads', file.filename)
        os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
        file.save(input_file_path)
        
        try:
            processed_data, json_data = transform_data_all(input_file_path)

            output_file_csv = os.path.join(project_root, 'data', 'clean', 'csv', f"cleaned_{os.path.basename(input_file_path)}")
            os.makedirs(os.path.dirname(output_file_csv), exist_ok=True)
            processed_data.to_csv(output_file_csv, index=False)

            with open(output_file_csv, 'r', encoding='utf-8') as csv_file:
                csv_content = csv_file.read()

            response = {
                "message": "success",
                "csv_content": csv_content,
                "json_content": json.dumps(json_data)
            }

            return jsonify(response), 200

        except Exception as e:
            import traceback
            return jsonify({
                "error": f"Error processing file: {str(e)}",
                "traceback": traceback.format_exc()
            }), 500
    else:
        return jsonify({"error": "Invalid file format. Only CSV files are allowed."}), 400


@app.route('/run_strategy', methods=['GET'])
def run_strategy():
    data = request.args.to_dict()
    print(data)
    year1, year2 = data["selected_strategy_year"].split("/")
    df = transform_data(f"data/sample/E0-{year1}{year2}.csv")
    team_id = team_mapping.get(data["selected_strategy_team"])
    keys_to_exclude = ["selected_strategy", "selected_strategy_team", "selected_strategy_year", "team"]
    filtered_params = {k: v for k, v in data.items() if k not in keys_to_exclude}
    bankroll, history = process_strategie(data["selected_strategy"], df, team_id, **filtered_params)
    response = {
        "status": "success",
        "bankroll": bankroll,
        "history": history
    }
    return jsonify(response)

@app.route('/run_strategy_all', methods=['GET'])
def run_strategy_all():
    data = request.args.to_dict()
    print(data)
    year1, year2 = data["selected_strategy_year"].split("/")
    df = transform_data(f"data/sample/E0-{year1}{year2}.csv")
    team_id = team_mapping.get(data["selected_strategy_team"])
    keys_to_exclude = ["selected_strategy", "selected_strategy_team", "selected_strategy_year", "team"]
    filtered_params = {k: v for k, v in data.items() if k not in keys_to_exclude}
    results = process_strategie_all(df, team_id, **filtered_params)
    response = {
        "status": "success",
        "result": results
    }
    return jsonify(response)

@app.route('/run_simulation', methods=['GET'])
def run_simulation():
    data = request.args.to_dict()
    home_team, away_team = data["HomeTeam"], data["AwayTeam"]
    home_odds, draw_odds, away_odds = data["HomeOdds"], data["DrawOdds"], data["AwayOdds"]
    year1, year2 = data["SelectedSimluationYear"].split("/")
    df = transform_data(f"data/sample/E0-{year1}{year2}.csv")
    home_team_id, away_team_id = team_mapping.get(home_team), team_mapping.get(away_team)
    home_win_prob, draw_prob, away_win_prob, over_2_5_prob, adjusted_home_win_odds, adjusted_draw_odds, adjusted_away_win_odds = simulation(df, home_team_id, away_team_id, market_home_win_odds=home_odds, market_draw_odds=draw_odds, market_away_win_odds=away_odds)
    
    response = {
        "home_win_prob": home_win_prob,
        "draw_prob": draw_prob,
        "away_win_prob": away_win_prob,
        "over_2_5_prob": over_2_5_prob,
        "adjusted_home_win_odds": adjusted_home_win_odds,
        "adjusted_draw_odds": adjusted_draw_odds,
        "adjusted_away_win_odds": adjusted_away_win_odds
    }
    return jsonify(response)

@app.route('/predict_odds', methods=['GET'])
def predict_odds():
    data = request.args.to_dict()

    data["HomeTeam"] = team_mapping.get(data["HomeTeam"])
    data["AwayTeam"] = team_mapping.get(data["AwayTeam"])

    win_pred, over25_odds_pred, over25_pred, home_odds_pred, away_odds_pred = predict(data)

    response = {
        "win_pred": next((key for key, value in team_mapping.items() if value == win_pred), None),
        "over25_odds_pred": over25_odds_pred,
        "over25_pred": over25_pred,
        "home_odds_pred": home_odds_pred,
        "away_odds_pred": away_odds_pred
    }

    return jsonify(response)

@app.route('/arbitrage_calculator', methods=['GET'])
def arbitrage_calculator_route():
    odd1 = float(request.args.get('odd1'))
    odd2 = float(request.args.get('odd2'))

    stake1, stake2, profit, is_arbitrage = arbitrage_calculator(odd1, odd2)

    print(is_arbitrage)
    
    return jsonify({
        "stake1": stake1,
        "stake2": stake2,
        "profit": profit,
        "is_arbitrage": is_arbitrage
    })


@app.route('/ev_calculator', methods=['GET'])
def ev_calculator_route():
    odds = float(request.args.get('odds'))
    probability = float(request.args.get('probability'))
    stake = float(request.args.get('stake'))
    
    ev, is_profitable = ev_calculator(odds, probability, stake)
    
    return jsonify({
        "expected_value": ev,
        "is_profitable": is_profitable
    })


@app.route('/expected_profit_calculator', methods=['GET'])
def expected_profit_calculator_route():
    odds = [float(x) for x in request.args.getlist('odds')]
    stakes = [float(x) for x in request.args.getlist('stakes')]
    probabilities = [float(x) for x in request.args.getlist('probabilities')]
    
    expected_profit = expected_profit_calculator(odds, stakes, probabilities)
    
    return jsonify({
        "expected_profit": expected_profit
    })


@app.route('/arbitrage_profit_percentage', methods=['GET'])
def arbitrage_profit_percentage_route():
    odd1 = float(request.args.get('odd1'))
    odd2 = float(request.args.get('odd2'))
    
    profit_percentage = arbitrage_profit_percentage(odd1, odd2)
    
    return jsonify({
        "profit_percentage": profit_percentage
    })


@app.route('/adjust_arbitrage_stakes', methods=['GET'])
def adjust_arbitrage_stakes_route():
    odd1 = float(request.args.get('odd1'))
    odd2 = float(request.args.get('odd2'))
    total_stake = float(request.args.get('total_stake'))
    
    stake1, stake2 = adjust_arbitrage_stakes(odd1, odd2, total_stake)
    
    return jsonify({
        "stake1": stake1,
        "stake2": stake2
    })

@app.route('/isArbitrage', methods=['GET'])
def find_is_arbitrage():
    odds_list = [float(x) for x in request.args.getlist('odds')]
    
    opportunities = find_arbitrage_opportunity(odds_list)
    
    return jsonify({
        "opportunities": opportunities
    })

@app.route('/find_arbitrage_opportunity', methods=['GET'])
def find_arbitrage_opportunity_route():
    odds_list = [float(x) for x in request.args.getlist('odds')]
    
    opportunities = find_arbitrage_opportunity(odds_list)
    
    return jsonify({
        "opportunities": opportunities
    })


@app.route('/arbitrage_bet_result', methods=['GET'])
def arbitrage_bet_result_route():
    odds1 = float(request.args.get('odds1'))
    odds2 = float(request.args.get('odds2'))
    stake1 = float(request.args.get('stake1'))
    stake2 = float(request.args.get('stake2'))
    outcome = request.args.get('outcome')

    result = arbitrage_bet_result(odds1, odds2, stake1, stake2, outcome)

    return jsonify({
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True)


