from modules.order import Order
from modules.orderbook import OrderBook
from modules.constants import *
import json
import random


def create_order_list(output_file: str = default_data_file) -> list[Order]:
    """
    :param output_file:             JSON file containing serialized orders
    :return:                        list of order objects

    Creates a list of orders from a given file.
    """

    orders = []
    try:
        with open(output_file) as json_file:
            orders_data = json.load(json_file)
            for order_data in orders_data:
                order = Order(json.dumps(order_data))
                orders.append(order)
    except json.JSONDecodeError as error:
        print("JSON decoder error: " + str(error))

    return orders


def create_order_book_from_orders_list(orders: list[Order], print_output: bool = False) -> OrderBook:
    """
    :param orders:                  list of orders
    :param print_output:            shows single transactions and order book states
    :return:                        order book object with realized transactions according to given orders

    Creates an order book object from a list of order objects
    and performs transactions for the orders if possible.
    """

    order_book = OrderBook(store_transactions=print_output)
    for order in orders:
        order_book.add(order)
        if print_output:
            print(">> " + order.__str__(simple=False))
            print(order_book)

    return order_book


def generate_random_orders(number_of_orders: int, iceberg_probability: float = default_iceberg_probability,
                           price_mean: int = default_price_mean, price_deviation: int = default_price_deviation,
                           quantity_mean: int = default_quantity_mean,
                           quantity_deviation: int = default_quantity_deviation,
                           peak_min: int = default_peak_min, peak_max: int = default_peak_max,
                           output_file: str = default_data_file):
    """
    :param number_of_orders:        the total number of orders
    :param iceberg_probability:     the expected relative amount of iceberg type orders
    :param price_mean:              normal distribution mean for 'price' field
    :param price_deviation:         standard deviation for 'price' field
    :param quantity_mean:           normal distribution mean for 'quantity' field
    :param quantity_deviation:      standard deviation for 'quantity' field
    :param peak_min:                minimum value of 'peak' field
    :param peak_max:                maximum value of 'peak' field
    :param output_file:             output file name

    Generates a series of random transactions to a JSON file.
    """

    orders = []
    print("Generating data...")
    for i in range(number_of_orders):
        order_type = "Limit"
        direction = "Buy" if random.random() < 0.5 else "Sell"

        peak = 0
        quantity = _generate(quantity_mean, quantity_deviation, random.normalvariate)
        if random.random() < iceberg_probability:
            order_type = "Iceberg"
            peak = min(_generate(peak_min, peak_max, random.uniform), quantity // 2)

        price = _generate(price_mean, price_deviation, random.normalvariate)
        orders.append(Order((i + 1, order_type, direction, price, quantity, peak)).__dict__(simple=False))

    print("Generated data. Saving to " + output_file + " file...")
    with open(output_file, 'w') as file:
        json.dump(orders, file, indent=4)


def _generate(alpha, beta, random_function) -> int:
    """
    :param alpha:                   first parameter of random_function
    :param beta:                    second parameter of random_function
    :param random_function:         generating function
    :return:                        random number according to random function distribution,
                                    rounded to multiplicities of 10

    Generates a random number for given random function with alpha and beta parameters.
    """
    return int(round(max(10., random_function(alpha, beta)), -1))
