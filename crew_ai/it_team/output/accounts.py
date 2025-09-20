class Account:
    def __init__(self, initial_deposit: float) -> None:
        if initial_deposit <= 0:
            raise ValueError('Initial deposit must be positive.')
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be positive.')
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError('Withdrawal amount must be positive.')
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        return True

    def buy_shares(self, symbol: str, quantity: int, share_price_func) -> bool:
        if quantity <= 0:
            raise ValueError('Quantity must be positive.')
        share_price = share_price_func(symbol)
        total_cost = share_price * quantity
        if total_cost > self.balance:
            return False
        self.balance -= total_cost
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity})
        return True

    def sell_shares(self, symbol: str, quantity: int, share_price_func) -> bool:
        if quantity <= 0:
            raise ValueError('Quantity must be positive.')
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            return False
        share_price = share_price_func(symbol)
        self.balance += share_price * quantity
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity})
        return True

    def get_portfolio_value(self, share_price_func) -> float:
        total_value = 0.0
        for symbol, quantity in self.portfolio.items():
            total_value += share_price_func(symbol) * quantity
        return total_value

    def get_profit_or_loss(self, share_price_func) -> float:
        current_value = self.get_portfolio_value(share_price_func)
        return (self.balance + current_value) - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.portfolio.copy()

    def get_transaction_history(self) -> list:
        return self.transactions.copy()

def get_share_price(symbol):
    prices = {
        'AAPL': 150.00,
        'TSLA': 600.00,
        'GOOGL': 2800.00,
    }
    return prices.get(symbol, 0.0)