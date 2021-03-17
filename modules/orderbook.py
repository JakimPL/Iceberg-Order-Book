from modules.order import Order
from sortedcontainers import SortedList
import json


class OrderBook:
    last_transactions: list[str] = []
    __timestamp: id = 0
    __store_transactions: bool = False
    __buy_orders: SortedList[Order] = SortedList()
    __sell_orders: SortedList[Order] = SortedList()

    def __init__(self, store_transactions=False):
        """
        :param store_transactions:  the flag for storing last performed transactions

        Initializes the order book. If 'store_transactions' is true,
        stores information about performed transactions
        in order to print them via the standard output.
        """

        self.__store_transactions = store_transactions
        self.__buy_orders = SortedList()
        self.__sell_orders = SortedList()

    def __repr__(self):
        """
        :return:                    string representation of the order book

        Returns a string of current order book state and latest transactions.
        """

        output = self.get_state() + "\n"
        if self.last_transactions:
            output += '\n'.join(self.last_transactions) + "\n"
        return output

    def add(self, order: Order):
        """
        :param order:               order being added to the order book

        Adds an order to the order book.
        Executes all possible transactions if possible
        and then returns the order book state.
        """

        order.timestamp = self.__get_timestamp()
        self.__get_orders_list(order).add(order)
        self.last_transactions.clear()

        while order.quantity > 0:
            matched_order = self.__match_order(order)
            if matched_order:
                self.__make_transaction(order, matched_order)
                self.__refresh_order(order)
            else:
                break

    def cancel(self, order: Order):
        """
        :param order:               order being removed

        Cancels a specific order, i.e. removes it from the order book.
        Raises a ValueError if there is no order of given id.
        """

        self.__get_orders_list(order).remove(order)

    def get_state(self) -> str:
        """
        :return:                    string of current order book status

        Returns the current order book status.
        """

        return json.dumps({'buyOrders': self.__serialize(self.__buy_orders),
                           'sellOrders': self.__serialize(self.__sell_orders)})

    def __match_order(self, new_order: Order):
        """
        :param new_order:           order to match
        :return:                    the best order if present None otherwise

        Matches best offers for a given order.
        If there is no such order, returns None object.
        """

        orders = self.__get_orders_list(new_order, swap_lists=True)

        if orders:
            order = orders[0]
            if order < new_order:
                return order

        return None

    def __get_orders_list(self, order: Order, swap_lists: bool = False) -> SortedList[Order]:
        """
        :param order:               given order
        :param swap_lists:          returns the opposite list if true
        :return:                    order book list of orders

        Returns the order book lists of orders of the same direction.
        If 'swap_lists' is true, the list of orders of opposed direction is returned.
        """

        if order.direction == "Buy":
            return self.__sell_orders if swap_lists else self.__buy_orders
        elif order.direction == "Sell":
            return self.__buy_orders if swap_lists else self.__sell_orders

    def __get_timestamp(self):
        """
        :return:                    current time

        Increases the global time and returns its value (as an integer).
        """

        self.__timestamp += 1
        return self.__timestamp

    def __make_transaction(self, order: Order, matched_order: Order):
        """
        :param order:               entered order
        :param matched_order:       order matched by engine

        Performs a single transaction.
        Raises ValueError if the transactions are of the same direction.
        """

        if order.direction == matched_order.direction:
            raise ValueError("can't perform a transaction of orders of the same direction")

        quantity = min(order.quantity, matched_order.quantity)

        order.quantity -= quantity
        matched_order.quantity -= quantity

        if matched_order.quantity == 0:
            self.__refresh_order(matched_order)

        if self.__store_transactions:
            if order.direction == "Buy":
                output_dict = {'buyOrderId': order.id, 'sellOrderId': matched_order.id}
            else:
                output_dict = {'buyOrderId': matched_order.id, 'sellOrderId': order.id}
            price_and_quantity_dict = {'price': matched_order.price, 'quantity': quantity}
            self.last_transactions.append(json.dumps({**output_dict, **price_and_quantity_dict}))

    def __refresh_order(self, order: Order):
        """
        :param order:               order to refresh

        Refreshes the order if its visible quantity is exhausted.
        If the real quantity is exhausted, removes from the list.
        """

        if order.quantity == 0:
            orders_list = self.__get_orders_list(order)
            orders_list.remove(order)
            if order.hidden_quantity > 0:
                order.timestamp = self.__get_timestamp()
                difference = min(order.peak, order.hidden_quantity)
                order.quantity += difference
                order.hidden_quantity -= difference
                orders_list.add(order)

    @staticmethod
    def __serialize(order_list: SortedList[Order]) -> list[dict]:
        """
        :param order_list:          sorted list of orders
        :return:                    list of orders as dictionary objects

        Returns the list of (simplified) orders' information, as dictionary objects.
        """

        return [order.__dict__() for order in order_list]
