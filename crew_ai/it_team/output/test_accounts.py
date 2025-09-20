import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(1000.0)

    def test_initial_deposit(self):
        self.assertEqual(self.account.balance, 1000.0)

    def test_initial_deposit_invalid(self):
        with self.assertRaises(ValueError):
            Account(-500.0)
            
    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)

    def test_deposit_invalid(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    def test_withdraw(self):
        result = self.account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 800.0)

    def test_withdraw_insufficient_funds(self):
        result = self.account.withdraw(2000.0)
        self.assertFalse(result)

    def test_withdraw_invalid(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)

    def test_buy_shares(self):
        result = self.account.buy_shares('AAPL', 2, get_share_price)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.portfolio['AAPL'], 2)

    def test_buy_shares_insufficient_balance(self):
        self.account.withdraw(800.0)  # Withdraw to leave only 200
        result = self.account.buy_shares('AAPL', 2, get_share_price)
        self.assertFalse(result)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 2, get_share_price)
        result = self.account.sell_shares('AAPL', 1, get_share_price)
        self.assertTrue(result)
        self.assertEqual(self.account.portfolio['AAPL'], 1)
        self.assertEqual(self.account.balance, 850.0)

    def test_sell_shares_insufficient_quantity(self):
        result = self.account.sell_shares('AAPL', 1, get_share_price)
        self.assertFalse(result)

    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 2, get_share_price)
        self.assertEqual(self.account.get_portfolio_value(get_share_price), 300.0)

    def test_get_profit_or_loss(self):
        self.account.buy_shares('AAPL', 2, get_share_price)
        self.assertEqual(self.account.get_profit_or_loss(get_share_price), -700.0)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 2, get_share_price)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})

    def test_get_transaction_history(self):
        self.account.deposit(200.0)
        self.account.withdraw(100.0)
        self.account.buy_shares('AAPL', 1, get_share_price)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 3)

if __name__ == '__main__':
    unittest.main()