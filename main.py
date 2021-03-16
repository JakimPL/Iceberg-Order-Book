#!/usr/bin/python
from modules.constants import default_data_file, program_description
from modules.order import Order
from modules.orderbook import OrderBook
from modules.timer import Timer
from modules.auxiliary import create_order_list, generate_random_orders, create_order_book_from_orders_list
from argparse import ArgumentParser, RawTextHelpFormatter
import sys


parser = ArgumentParser(description=program_description + """
Usage:
        python main.py
for a line-by-line input or
        python main.py [input]
for a serialized JSON file, eg.
        python main.py example.json -s
'-s' flag prints each transaction.

In order to generate list of orders and the save to file, use:
        python main.py -g [number] -o [file]
eg.:
        python main.py -g 100000 -o random_orders.json
If the output is not specified, the default one is used.
""", formatter_class=RawTextHelpFormatter)
parser.add_argument('input', metavar='input', type=str, nargs='?', default="",
                    help='reads JSON file with serialized orders')
parser.add_argument('-g', '--generate-orders', metavar='number_of_transactions', type=int, nargs=1, default=[0],
                    help='generates random orders data to a file (' + default_data_file + ' by default)')
parser.add_argument('-o', '--output', metavar='output', type=str, nargs='?', default=None,
                    help='saves generated random orders to a specific file')
parser.add_argument('-s', '--show-details', dest='show_details', action='store_true',
                    help='shows the list of the transactions')

# parse program arguments
args = parser.parse_args()
input_file: str = args.input
output_file: str = args.output
number_of_transactions: int = args.generate_orders[0]
show_details: bool = args.show_details

# run the timer to measure performance
timer = Timer()

if output_file and number_of_transactions <= 0:
    print("In order to generate random data, '-g [number]' option on has to be present.")
    sys.exit(0)

if number_of_transactions > 0:
    """ Generates random transactions and saves them to JSON file. """
    if input_file:
        print("WARNING: '" + str(input_file) + "' argument is omitted.\n"
                                               "To specify an output path use '-o [output]' option.\n")

    if not output_file:
        output_file = default_data_file

    orders = generate_random_orders(number_of_transactions, output_file=output_file)
    delta_time = timer()
    print("Generated {0} orders in {1} seconds. Saved data to {2}.".format(
        number_of_transactions, delta_time, output_file))
    sys.exit(0)

if input_file:
    """ Parse JSON file and load to memory. """
    print("Parsing {0}...".format(input_file))
    orders = create_order_list(input_file)
    delta_time = timer()
    print("Loaded {0} in {1} seconds.".format(input_file, delta_time))

    number_of_transactions = len(orders)
    order_book = create_order_book_from_orders_list(orders, print_output=show_details)

    delta_time = timer()
    print("\nFinal order book state:\n" + order_book.get_state())
    print("\nElapsed time: {0} seconds.".format(delta_time))
    print("{:.2f} orders per second.".format(number_of_transactions / delta_time))
    sys.exit(0)

# run the main program if no special branch has been activated
order_book = OrderBook(store_transactions=True)
print(program_description + """
To add an order to the order book, insert a JSON line.
Type 'exit' to quit the program.\n""")

try:
    for line in sys.stdin:
        if bool(line and not line.isspace()):
            if "exit" in line:
                break

            order = Order(line)

            # we assume that id cannot be negative
            if order.id >= 0:
                order_book.add(order)
                print(order_book)
except KeyboardInterrupt:
    pass

print("\nSession ended.")
