import json


program_description = "An order book implementation with limit and iceberg type orders."

with open("config.json") as config_json:
    config_data = json.load(config_json)

default_data_file = config_data['default_output']
default_iceberg_probability = config_data['iceberg_probability']
default_price_mean = config_data['price_mean']
default_price_deviation = config_data['price_deviation']
default_quantity_mean = config_data['quantity_mean']
default_quantity_deviation = config_data['quantity_deviation']
default_peak_min = config_data['peak_min']
default_peak_max = config_data['peak_max']
