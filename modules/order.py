import json


class Order:
    id: int = -1
    timestamp: int = 0
    direction: str
    type: str
    price: int
    quantity: int
    hidden_quantity: int
    peak: int

    def __dict__(self, simple: bool = True):
        """
        Returns a dictionary object from an order object.
        If 'simple' flag is true, returns a simplified version of the order's dictionary object.
        """

        if simple:
            return {'id': self.id, 'price': self.price, 'quantity': self.quantity}
        else:
            order_info = {'direction': self.direction, 'id': self.id, 'price': self.price, 'quantity': self.quantity}
            if self.peak > 0:
                order_info['peak'] = self.peak
            return {'type': self.type, 'order': order_info}

    def __init__(self, input_data):
        """
        Create an order object from either JSON line
        or a tuple of the form (id, type, direction, price, quantity, peak).
        """

        if isinstance(input_data, str):
            data = json.loads(input_data)
            order_data = data['order']

            self.type = data['type']
            self.direction = order_data['direction']
            self.id = order_data['id']
            self.price = order_data['price']
            self.quantity = order_data['quantity']
            if self.type == "Iceberg" and 'peak' in order_data:
                self.peak = order_data['peak']
            else:
                self.peak = 0

        elif isinstance(input_data, tuple):
            self.id, self.type, self.direction, self.price, self.quantity, self.peak = input_data

        else:
            raise TypeError("expected a JSON line or a tuple")

        self.timestamp = self.id
        if self.peak > 0:
            if self.type == "Limit":
                raise ValueError("limit orders can't have a positive 'peak'")
            self.hidden_quantity = max(self.quantity - self.peak, 0)
            self.quantity = min(self.quantity, self.peak)
        else:
            if self.type == "Iceberg":
                raise ValueError("iceberg orders can't have zero 'peak'")

            self.hidden_quantity = 0

        if self.price == 0 or self.quantity == 0:
            raise ValueError('price of the order cannot be zero')

    def __eq__(self, other):
        """
        Returns true if two orders are the same: they share the same fields.
        If there are different but they share the same id, ValueError is raised.
        """

        if self.id == other.id:
            if self.price == other.price and self.quantity == other.quantity and self.peak == other.peak and \
               self.direction == other.direction and self.type == other.type:
                return True
            else:
                raise ValueError("different orders share the same id")
        else:
            return False

    def __lt__(self, other):
        """
        Compares two orders by price with non-increasing order for 'Buy' orders
        and non-decreasing for 'Sell' orders.
        """

        if self.price != other.price:
            return (self.price < other.price) ^ (self.direction == "Buy")
        else:
            return self.timestamp < other.timestamp

    def __str__(self, simple: bool = True):
        """
        Returns a dictionary string of an order object.
        If 'simple' flag is true, returns a simplified string
        with hidden real quantity in case of iceberg orders.
        """

        return str(self.__dict__(simple))

    def return_json(self):
        """
        Returns a JSON object from an order object.
        Uses a object -> dictionary conversion.
        """

        return json.dumps(self.__dict__())
