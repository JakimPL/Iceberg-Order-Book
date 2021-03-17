import unittest
from modules.order import Order


class TestOrderInput(unittest.TestCase):
    def test_correct_limit_tuple(self):
        order = Order((1, "Limit", "Buy", 100, 100, 0))
        self.assertEqual(order.id, 1)
        self.assertEqual(order.type, "Limit")
        self.assertEqual(order.direction, "Buy")
        self.assertEqual(order.quantity, 100)
        self.assertEqual(order.hidden_quantity, 0)
        self.assertEqual(order.price, 100)

    def test_correct_limit_json(self):
        order = Order('{"type": "Limit", "order":'
                      '{"direction": "Buy", "id": 1, "price": 100, "quantity": 100}}')
        self.assertEqual(order.id, 1)
        self.assertEqual(order.type, "Limit")
        self.assertEqual(order.direction, "Buy")
        self.assertEqual(order.quantity, 100)
        self.assertEqual(order.hidden_quantity, 0)
        self.assertEqual(order.price, 100)

    def test_correct_iceberg_tuple(self):
        order = Order((1, "Iceberg", "Buy", 100, 100, 10))
        self.assertEqual(order.id, 1)
        self.assertEqual(order.type, "Iceberg")
        self.assertEqual(order.direction, "Buy")
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.hidden_quantity, 90)
        self.assertEqual(order.price, 100)
        self.assertEqual(order.peak, 10)

    def test_correct_iceberg_json(self):
        order = Order('{"type": "Iceberg", "order":'
                      '{"direction": "Buy", "id": 1, "price": 100, "quantity": 100, "peak": 10}}')
        self.assertEqual(order.id, 1)
        self.assertEqual(order.type, "Iceberg")
        self.assertEqual(order.direction, "Buy")
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.hidden_quantity, 90)
        self.assertEqual(order.price, 100)
        self.assertEqual(order.peak, 10)

    def test_limit_wrong_sized_tuple(self):
        self.assertRaises(ValueError, Order, (1, "Limit", "Buy", 100, 100))
        self.assertRaises(ValueError, Order, (1, "Limit", "Buy", 100, 100, 0, 0))

    def test_limit_positive_peak_tuple(self):
        self.assertRaises(ValueError, Order, (1, "Limit", "Buy", 100, 100, 10))

    def test_limit_positive_peak_json(self):
        order = Order('{"type": "Limit", "order":'
                      '{"direction": "Buy", "id": 1, "price": 100, "quantity": 100, "peak": 10}}')
        self.assertEqual(order.peak, 0)

    def test_iceberg_zero_peak_tuple(self):
        self.assertRaises(ValueError, Order, (1, "Iceberg", "Buy", 100, 100, 0))

    def test_limit_zero_peak_json(self):
        json_line = '{"type": "Iceberg","order":' \
                    '{"direction": "Buy", "id": 1, "price": 100, "quantity": 100, "peak": 0}}'
        self.assertRaises(ValueError, Order, json_line)

    def test_limit_zero_price_tuple(self):
        self.assertRaises(ValueError, Order, (1, "Limit", "Sell", 0, 100, 0))

    def test_limit_zero_price_json(self):
        json_line = '{"type": "Limit","order":' \
                    '{"direction": "Buy", "id": 1, "price": 0, "quantity": 100}}'
        self.assertRaises(ValueError, Order, json_line)

    def test_limit_zero_quantity_tuple(self):
        self.assertRaises(ValueError, Order, (1, "Limit", "Sell", 100, 0, 0))

    def test_limit_zero_quantity_json(self):
        json_line = '{"type": "Limit","order":' \
                    '{"direction": "Buy", "id": 1, "price": 100, "quantity": 0}}'
        self.assertRaises(ValueError, Order, json_line)

    def test_limit_no_price_json(self):
        json_line = '{"type": "Limit","order":' \
                    '{"direction": "Sell", "id": 1, "quantity": 100}}'
        self.assertRaises(KeyError, Order, json_line)

    def test_limit_no_quantity_json(self):
        json_line = '{"type": "Limit","order":' \
                    '{"direction": "Sell", "id": 1, "price": 100}}'
        self.assertRaises(KeyError, Order, json_line)

    def test_limit_no_id_json(self):
        json_line = '{"type": "Limit","order":' \
                    '{"direction": "Buy", "price": 0, "quantity": 100}}'
        self.assertRaises(KeyError, Order, json_line)

    def test_limit_no_direction_json(self):
        json_line = '{"type": "Limit","order":' \
                    '{"id": 1, "price": 100, "quantity": 100}}'
        self.assertRaises(KeyError, Order, json_line)

    def test_iceberg_no_peak_json(self):
        json_line = '{"type": "Iceberg","order":' \
                    '{"direction": "Buy", "id": 1, "price": 100, "quantity": 100}}'
        self.assertRaises(ValueError, Order, json_line)


if __name__ == '__main__':
    unittest.main()
