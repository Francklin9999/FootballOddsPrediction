def arbitrage_calculator(odd1, odd2):
    prob1 = 1 / odd1
    prob2 = 1 / odd2
    total_prob = prob1 + prob2

    stake1 = round(prob1 / total_prob, 2)
    stake2 = round(prob2 / total_prob, 2)
    profit = round(1 - total_prob, 2)

    return stake1, stake2, profit, total_prob < 1

def ev_calculator(odds, probability, stake):
    payout = (odds * stake) - stake
    ev = round((probability * payout) - ((1 - probability) * stake), 2)
    
    return ev, ev > 0

def expected_profit_calculator(odds, stakes, probabilities):
    total_payout = sum(odds[i] * stakes[i] for i in range(len(odds)))
    total_cost = sum(stakes)

    expected_profit = round(total_payout - total_cost, 2)

    return expected_profit

def arbitrage_profit_percentage(odd1, odd2):
    prob1 = 1 / odd1
    prob2 = 1 / odd2
    total_prob = prob1 + prob2

    if total_prob >= 1:
        return 0

    profit_percentage = round((1 - total_prob) * 100, 2)
    
    return profit_percentage

def adjust_arbitrage_stakes(odd1, odd2, total_stake):
    prob1 = 1 / odd1
    prob2 = 1 / odd2
    total_prob = prob1 + prob2

    stake1 = round((prob1 / total_prob) * total_stake, 2)
    stake2 = round((prob2 / total_prob) * total_stake, 2)

    return stake1, stake2

def find_arbitrage_opportunity(odds_list):
    opportunities = []

    for i in range(len(odds_list)):
        for j in range(i + 1, len(odds_list)):
            odd1 = odds_list[i]
            odd2 = odds_list[j]
            prob1 = 1 / odd1
            prob2 = 1 / odd2
            total_prob = prob1 + prob2
            
            if total_prob < 1:
                opportunities.append((odd1, odd2))

    return opportunities

def arbitrage_bet_result(odds1, odds2, stake1, stake2, outcome):
    if outcome == "home":
        return round(odds1 * stake1 - stake1, 2)
    elif outcome == "away":
        return round(odds2 * stake2 - stake2, 2)
    else:
        return 0 


# print(arbitrage_calculator(1.55, 2.10))