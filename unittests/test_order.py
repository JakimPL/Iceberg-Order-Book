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

    def test_order_simple_dictionary(self):
        order = Order((1, "Iceberg", "Sell", 30, 100, 10))
        order_dictionary = order.__dict__()

        self.assertEqual(order_dictionary.get('id'), 1)
        self.assertEqual(order_dictionary.get('price'), 30)
        self.assertEqual(order_dictionary.get('quantity'), 10)
        self.assertEqual(order_dictionary.get('peak'), None)
        self.assertEqual(order_dictionary.get('direction'), None)
        self.assertEqual(order_dictionary.get('type'), None)

    def test_order_detailed_dictionary(self):
        order = Order((1, "Iceberg", "Sell", 30, 100, 10))
        order_dictionary = order.__dict__(simple=False)
        order_info_dictionary = order_dictionary.get('order')

        self.assertEqual(order_info_dictionary.get('id'), 1)
        self.assertEqual(order_info_dictionary.get('price'), 30)
        self.assertEqual(order_info_dictionary.get('quantity'), 10)
        self.assertEqual(order_info_dictionary.get('peak'), 10)
        self.assertEqual(order_info_dictionary.get('direction'), "Sell")
        self.assertEqual(order_dictionary.get('type'), "Iceberg")


if __name__ == '__main__':
    unittest.main()
