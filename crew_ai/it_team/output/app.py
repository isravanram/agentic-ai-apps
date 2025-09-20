import gradio as gr
from accounts import Account, get_share_price

# Initialize account with an initial deposit
account = Account(initial_deposit=1000)

def create_account(initial_deposit):
    global account
    account = Account(initial_deposit)
    return f"Account created with initial deposit: ${initial_deposit}"

def deposit_funds(amount):
    account.deposit(amount)
    return f"Deposited: ${amount}. Current balance: ${account.balance}"

def withdraw_funds(amount):
    if account.withdraw(amount):
        return f"Withdrew: ${amount}. Current balance: ${account.balance}"
    return "Withdrawal failed. Insufficient balance."

def buy_shares(symbol, quantity):
    if account.buy_shares(symbol, quantity, get_share_price):
        return f"Bought {quantity} shares of {symbol}. Current portfolio: {account.get_holdings()}"
    return "Buy failed. Not enough funds or invalid quantity."

def sell_shares(symbol, quantity):
    if account.sell_shares(symbol, quantity, get_share_price):
        return f"Sold {quantity} shares of {symbol}. Current portfolio: {account.get_holdings()}"
    return "Sell failed. Not enough shares or invalid quantity."

def portfolio_value():
    value = account.get_portfolio_value(get_share_price)
    return f"Total portfolio value: ${value}"

def profit_or_loss():
    profit_loss = account.get_profit_or_loss(get_share_price)
    return f"Profit/Loss: ${profit_loss}"

def transaction_history():
    history = account.get_transaction_history()
    return history if history else "No transactions recorded."

inputs = [
    gr.inputs.Number(label="Initial Deposit", default=1000),
    gr.inputs.Number(label="Deposit Amount", default=100),
    gr.inputs.Number(label="Withdraw Amount", default=100),
    gr.inputs.Textbox(label="Buy Symbol (AAPL, TSLA, GOOGL)"),
    gr.inputs.Number(label="Buy Quantity", default=1),
    gr.inputs.Textbox(label="Sell Symbol (AAPL, TSLA, GOOGL)"),
    gr.inputs.Number(label="Sell Quantity", default=1),
]

outputs = [
    gr.outputs.Textbox(label="Create Account Output"),
    gr.outputs.Textbox(label="Deposit Output"),
    gr.outputs.Textbox(label="Withdraw Output"),
    gr.outputs.Textbox(label="Buy Output"),
    gr.outputs.Textbox(label="Sell Output"),
    gr.outputs.Textbox(label="Portfolio Value Output"),
    gr.outputs.Textbox(label="Profit/Loss Output"),
    gr.outputs.Textbox(label="Transaction History Output"),
]

def main(initial_deposit, deposit_amount, withdraw_amount, buy_symbol, buy_quantity, sell_symbol, sell_quantity):
    create_output = create_account(initial_deposit)
    deposit_output = deposit_funds(deposit_amount)
    withdraw_output = withdraw_funds(withdraw_amount)
    buy_output = buy_shares(buy_symbol, buy_quantity)
    sell_output = sell_shares(sell_symbol, sell_quantity)
    value_output = portfolio_value()
    profit_output = profit_or_loss()
    history_output = transaction_history()
    
    return create_output, deposit_output, withdraw_output, buy_output, sell_output, value_output, profit_output, history_output

gr.Interface(fn=main, inputs=inputs, outputs=outputs, title="Trading Account Management").launch()