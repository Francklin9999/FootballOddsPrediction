import inspect

# Double your bet after each loss to recover losses
def martingale_strategy(df, team_id, bankroll, base_bet):
    bankroll = float(bankroll)
    base_bet = float(base_bet)
    bet = base_bet
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet
            bet = base_bet
        else:
            bankroll -= bet
            bet *= 2
        history[idx] = round(bankroll, 2)
        idx += 1
    return round(bankroll, 2), history

# Double your bet after a win to ride winning streaks
def anti_martingale_strategy(df, team_id, bankroll, base_bet):
    bankroll = float(bankroll)
    base_bet = float(base_bet)
    bet = base_bet
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet
            bet *= 2
        else:
            bankroll -= bet
            bet = base_bet
        history[idx] = round(bankroll, 2)
        idx += 1
                
    return round(bankroll, 2), history

# Increase bets following the Fibonacci sequence after losses
def fibonacci_strategy(df, team_id, bankroll, base_bet):
    bankroll = float(bankroll)
    base_bet = float(base_bet)
    fib_seq = [1, 1]
    bet_index = 0
    bet = base_bet * fib_seq[bet_index]
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet
            bet_index = max(0, bet_index - 2)
        else:
            bankroll -= bet
            bet_index += 1
            if bet_index >= len(fib_seq):
                fib_seq.append(fib_seq[-1] + fib_seq[-2])
        bet = base_bet * fib_seq[bet_index]
        history[idx] = round(bankroll, 2)
        idx += 1
    return round(bankroll, 2), history

# Increase bets by a fixed unit after a loss and decrease after a win
def dalembert_strategy(df, team_id, bankroll, base_bet):
    bankroll = float(bankroll)
    base_bet = float(base_bet)
    bet = base_bet
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet
            bet = max(base_bet, bet - base_bet)
        else:
            bankroll -= bet
            bet += base_bet
        history[idx] = round(bankroll, 2)
        idx += 1
    return round(bankroll, 2), history

# A slow progression system increasing bets after a win but keeping them steady after a loss
def oscars_grind_strategy(df, team_id, bankroll, base_bet):
    bankroll = float(bankroll)
    base_bet = float(base_bet)
    bet = base_bet
    profit = 0
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet
            profit += bet
            if profit < base_bet:
                bet += base_bet
        else:
            bankroll -= bet
        history[idx] = round(bankroll, 2)
        idx += 1
    return round(bankroll, 2), history

# Bet a consistent amount each time
def fixed_betting_strategy(df, team_id, bankroll, bet_amount):
    bankroll = float(bankroll)
    bet_amount = float(bet_amount)
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet_amount
        else:
            bankroll -= bet_amount
        history[i] = round(bankroll, 2)
        idx += 1
    return round(bankroll, 2), history

# Bet a fixed percentage of your bankroll
def percentage_betting_strategy(df, team_id, bankroll, percentage):
    bankroll = float(bankroll)
    percentage = float(percentage)
    history = {}
    idx = 1
    for i, match in df.iterrows():
        if bankroll <= 0:
            break
        bet = bankroll * percentage
        is_home = match["HomeTeam"] == team_id
        won = (match["FullTimeResult"] == 1 and is_home) or (match["FullTimeResult"] == 0 and not is_home)
        if won:
            bankroll += bet
        else:
            bankroll -= bet
        history[i] = round(bankroll, 2)
        idx += 1
    return round(bankroll, 2), history

def process_strategie(strategy, df, team_id, **kwargs):
    strategies = {
        "Martingale": martingale_strategy,
        "Anti-Martingale": anti_martingale_strategy,
        "Fibonacci": fibonacci_strategy,
        "D'Alembert": dalembert_strategy,
        "Oscar's Grind": oscars_grind_strategy,
        "Flat Betting": fixed_betting_strategy,
        "Percentage Betting": percentage_betting_strategy
    }
        
    df = df[(df["HomeTeam"] == team_id) | (df["AwayTeam"] == team_id)]

    strategy_function = strategies.get(strategy)

    if strategy_function:
        func_params = inspect.signature(strategy_function).parameters
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in func_params}
        return strategy_function(df, team_id, **filtered_kwargs)
    
def process_strategie_all(df, team_id, **kwargs):
    strategies = {
        "Martingale": martingale_strategy,
        "Anti-Martingale": anti_martingale_strategy,
        "Fibonacci": fibonacci_strategy,
        "D'Alembert": dalembert_strategy,
        "Oscar's Grind": oscars_grind_strategy,
        "Flat Betting": fixed_betting_strategy,
        "Percentage Betting": percentage_betting_strategy
    }
    
    df = df[(df["HomeTeam"] == team_id) | (df["AwayTeam"] == team_id)]
    
    results = {}

    for strategy, strategy_function in strategies.items():
        func_params = inspect.signature(strategy_function).parameters
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in func_params}

        bankroll, history = strategy_function(df, team_id, **filtered_kwargs)

        results[strategy] = {
            "bankroll": bankroll,
            "history": history
        }
    
    return results

