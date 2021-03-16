# Iceberg Order Book
An order book implementation with limit and iceberg type orders done in Python. Based on SortedList.

### Description

The order book supports two type of orders: *limit* orders and *iceberg* orders. Each order is stored as a JSON object containing:
* `type` indicating the type of the order: either *Limit* or *Iceberg*,
* `order` storing detailed information about the order:
	* `direction` either *Buy* or *Sell*,
	* `id` unique identifier (a positive integer) of the order,
	* `price` which is a positive integer,
	* `quantity` the amount of the order.
	* `peak` maximum visible amount for iceberg type orders, for limit orders this value is set to 0.

An example of: limit sell order and buy iceberg order:
```
{"type": "Limit", "order": {"direction": "Sell", "id": 1, "price": 100, "quantity": 200}}
{"type": "Iceberg", "order": {"direction": "Buy", "id": 2, "price": 100, "quantity": 300, "peak": 100}}
```

The order book is mainly based on `sortedcontainers` package.

## Usage

In order to start a session, type:
`python main.py`

Enter each JSON string (as in the example) in a single line to add an order to the order book. This results in a current order book state with a list with all performed transactions. For instance, after the input below:

```
{"type": "Limit", "order": {"direction": "Buy", "id": 1, "price": 10, "quantity": 30}}
{"type": "Iceberg", "order": {"direction": "Sell", "id": 2, "price": 10, "quantity": 50, "peak": 20}}
```

a following response will be displayed:

```
{"buyOrders": [{"id": 1, "price": 10, "quantity": 30}], "sellOrders": []}

{"buyOrders": [], "sellOrders": [{"id": 2, "price": 10, "quantity": 10}]}
{"buyOrderId": 1, "sellOrderId": 2, "price": 10, "quantity": 20}
{"buyOrderId": 1, "sellOrderId": 2, "price": 10, "quantity": 10}
```

So, after two transactions of corresponding quantities 20 and 10, there is a single *Sell* order in the order book.

To close the session one can type `exit`.

## Series of data

There is a possibility to run a series of data from a JSON file. An example is stored in the file `example.json`. To perform orders from a file use:

`python main.py [input]`

e.g. `python main.py example.json`. To see all intermediate order book states with all performed transactions, one can use `--show-details` (or simply `-s`) argument, e.g.:

`python main.py example.json -s`

## Random data

The order book provides a way to generate random data based on normal/uniform distribution. To generate a file use the following command:

`python main.py --generate-orders [number] --output [output]` or `python main.py -g [number] -o [output]`

where `number` stands for the number of orders and `output` is the output filename. If the output is not specified, the default filename is used (`data.json` by default). For example:

`python main.py -g 100000 -o random_orders.json`

generates a JSON file `random_orders.json` with 100000 random orders. To execute these orders `python main.py random_orders.json`.

Parameters of distributions such as:
* `iceberg_probability` - the expected relative amount of iceberg type orders,
* `price_mean` - normal distribution mean for *price* field,
* `price_deviation` - standard deviation for *price* field,
* `quantity_mean` - normal distribution mean for *quantity* field,
* `quantity_deviation` - standard deviation for *quantity* field,
* `peak_min` - minimum value of *peak* field,
* `peak_max` - maximum value of *peak* field

are stored in `config.json`.