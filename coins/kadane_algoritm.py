def get_profitable_periods(self, coin_prices):
    max_profit = 0
    current_profit = 0
    start = end = s = 0
    periods = []
    
    for i in range(1, len(coin_prices)):
        current_profit += coin_prices[i].price - coin_prices[i-1].price
        if current_profit > max_profit:
            max_profit = current_profit
            start = s
            end = i
        if current_profit < 0:
            current_profit = 0
            s = i

    if start != end:
        periods.append({
            'start': coin_prices[start],
            'end': coin_prices[end],
            'profit': max_profit
        })
    return periods



def get_loss_making_periods(self, coin_prices):
    max_loss = 0
    current_loss = 0
    start = end = s = 0
    periods = []
    
    for i in range(1, len(coin_prices)):
        current_loss += coin_prices[i-1].price - coin_prices[i].price
        if current_loss > max_loss:
            max_loss = current_loss
            start = s
            end = i
        if current_loss < 0:
            current_loss = 0
            s = i

    if start != end:
        periods.append({
            'start': coin_prices[start],
            'end': coin_prices[end],
            'loss': max_loss
        })
    return periods