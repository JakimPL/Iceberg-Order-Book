import unittest
from modules.order import Order


class TestOrderStructure(unittest.TestCase):
    def test_orders_of_the_same_id(self):
        order1 = Order((1, "Limit", "Buy", 100, 100, 0))
        order2 = Order((1, "Limit", "Buy", 200, 300, 0))
        self.assertRaises(ValueError, order1.__eq__, order2)

        order2 = Order((1, "Limit", "Buy", 100, 100, 0))
        self.assertEqual(order1, order2)

    def test_buy_order_comparison(self):
        order1 = Order((1, "Limit", "Buy", 20, 100, 0))
        order2 = Order((2, "Limit", "Buy", 30, 100, 0))
        self.assertLess(order2, order1)

        order2 = Order((2, "Limit", "Buy", 10, 100, 0))
        self.assertLess(order1, order2)

        order2 = Order((2, "Limit", "Buy", 20, 100, 0))
        self.assertLess(order1, order2)

    def test_sell_order_comparison(self):
        order1 = Order((1, "Limit", "Sell", 20, 100, 0))
        order2 = Order((2, "Limit", "Sell", 30, 100, 0))
        self.assertLess(order1, order2)

        order2 = Order((2, "Limit", "Sell", 10, 100, 0))
        self.assertLess(order2, order1)

        order2 = Order((2, "Limit", "Sell", 20, 100, 0))
        self.assertLess(order1, order2)


if __name__ == '__main__':
    unittest.main()
