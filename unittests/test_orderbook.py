import unittest
from modules.order import Order
from modules.orderbook import OrderBook


class TestOrderBook(unittest.TestCase):
    def test_order_book_add_order(self):
        order_book = OrderBook()
        order = Order((1, "Limit", "Buy", 100, 100, 0))
        order_book.add(order)
        self.assertEqual(order_book.get_state(),
                         '{"buyOrders": [{"id": 1, "price": 100, "quantity": 100}], "sellOrders": []}')

    def test_order_book_cancel_order(self):
        order_book = OrderBook()
        order = Order((1, "Limit", "Buy", 100, 100, 0))
        order_book.add(order)
        order_book.cancel(order)
        self.assertEqual(order_book.get_state(), '{"buyOrders": [], "sellOrders": []}')

    def test_order_book_cancel_not_present_order(self):
        order_book = OrderBook()
        order = Order((1, "Limit", "Buy", 100, 100, 0))
        order_book.add(order)
        order_book.cancel(order)
        self.assertRaises(ValueError, order_book.cancel, order)

    def test_order_book_not_storing_transactions(self):
        order_book = OrderBook(store_transactions=False)
        order_book.add(Order((1, "Limit", "Buy", 100, 100, 0)))
        self.assertEqual(order_book.last_transactions, [])

        order_book.add(Order((2, "Limit", "Sell", 100, 100, 0)))
        self.assertEqual(order_book.last_transactions, [])

        self.assertEqual(order_book.get_state(), '{"buyOrders": [], "sellOrders": []}')

    def test_order_book_limit_transactions(self):
        order_book = OrderBook(store_transactions=True)
        order_book.add(Order((1, "Limit", "Buy", 100, 100, 0)))
        self.assertEqual(order_book.last_transactions, [])

        order_book.add(Order((2, "Limit", "Sell", 80, 50, 0)))
        self.assertEqual(order_book.last_transactions,
                         ['{"buyOrderId": 1, "sellOrderId": 2, "price": 100, "quantity": 50}'])

        order_book.add(Order((3, "Limit", "Sell", 120, 40, 0)))
        self.assertEqual(order_book.last_transactions, [])

        self.assertEqual(order_book.get_state(),
                         '{"buyOrders": [{"id": 1, "price": 100, "quantity": 50}],'
                         ' "sellOrders": [{"id": 3, "price": 120, "quantity": 40}]}')

    def test_order_book_iceberg_transactions(self):
        order_book = OrderBook(store_transactions=True)
        orders = [
            '{"type": "Iceberg", "order": {"direction": "Sell", "id": 1, "price": 100, "quantity": 200, "peak": 100}}',
            '{"type": "Iceberg", "order": {"direction": "Sell", "id": 2, "price": 100, "quantity": 300, "peak": 100}}',
            '{"type": "Iceberg", "order": {"direction": "Sell", "id": 3, "price": 100, "quantity": 200, "peak": 100}}',
            '{"type": "Iceberg", "order": {"direction": "Buy",  "id": 4, "price": 100, "quantity": 500, "peak": 100}}'
        ]

        expected_states = [
            '{"buyOrders": [], "sellOrders": [{"id": 1, "price": 100, "quantity": 100}]}',

            '{"buyOrders": [], "sellOrders":'
            ' [{"id": 1, "price": 100, "quantity": 100}, {"id": 2, "price": 100, "quantity": 100}]}',

            '{"buyOrders": [], "sellOrders":'
            ' [{"id": 1, "price": 100, "quantity": 100}, {"id": 2, "price": 100, "quantity": 100},'
            ' {"id": 3, "price": 100, "quantity": 100}]}',

            '{"buyOrders": [], "sellOrders":'
            ' [{"id": 3, "price": 100, "quantity": 100}, {"id": 2, "price": 100, "quantity": 100}]}'
        ]

        expected_transactions = [
            [], [], [],
            ['{"buyOrderId": 4, "sellOrderId": 1, "price": 100, "quantity": 100}',
             '{"buyOrderId": 4, "sellOrderId": 2, "price": 100, "quantity": 100}',
             '{"buyOrderId": 4, "sellOrderId": 3, "price": 100, "quantity": 100}',
             '{"buyOrderId": 4, "sellOrderId": 1, "price": 100, "quantity": 100}',
             '{"buyOrderId": 4, "sellOrderId": 2, "price": 100, "quantity": 100}']
        ]

        for i in range(4):
            order_book.add(Order(orders[i]))
            self.assertEqual(order_book.get_state(), expected_states[i])
            self.assertEqual(order_book.last_transactions, expected_transactions[i])


if __name__ == '__main__':
    unittest.main()
