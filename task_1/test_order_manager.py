import unittest
from unittest.mock import MagicMock, patch
from order_manager import OrderManager

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.db_mock = MagicMock()
        self.manager = OrderManager(self.db_mock, 'smtp.test', 587, 0.1, 'USD')
        self.manager.users = {
            1: {'banned': False, 'email': 'good@test.com'},
            2: {'banned': True, 'email': 'bad@test.com'}
        }
        self.manager.inventory = {
            'item1': {'stock': 10, 'price': 100}
        }

    @patch('smtplib.SMTP')
    def test_create_order_success(self, mock_smtp):
        order = self.manager.create_order(1, {'item1': 2}, promo_code='SAVE10')
        
        self.assertAlmostEqual(order['total'], 198.0)
        self.assertEqual(self.manager.inventory['item1']['stock'], 8)
        self.db_mock.execute.assert_called_once()
        mock_smtp.return_value.sendmail.assert_called_once()

    def test_banned_user_raises_exception(self):
        with self.assertRaises(Exception) as context:
            self.manager.create_order(2, {'item1': 1})
        self.assertTrue('User is banned' in str(context.exception))
        
if __name__ == '__main__':
    unittest.main()