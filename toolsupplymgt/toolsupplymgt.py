import csv
import re
import pprint 
import os
import logging
import sys
import argparse


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

order_path = os.path.join(ROOT_DIR, 'data', 'orders.csv')
product_path = os.path.join(ROOT_DIR, 'data', 'products.csv')
customers_path = os.path.join(ROOT_DIR, 'data', 'customers.csv')

order_prices_path = os.path.join(ROOT_DIR, 'data', 'results', 'order_prices.csv')
product_customers_path = os.path.join(ROOT_DIR, 'data','results', 'product_customers.csv')
customer_ranking_path = os.path.join(ROOT_DIR, 'data', 'results','customer_ranking.csv')


def process_order(product_path, order_path ):
    product_lst = get_products_list(product_path)
    ordered_prices = {}
    ordered_prices_list = []
    try:
        with open(order_path, 'r', newline='') as f:
            order_reader = csv.DictReader(f)
            try:
                for order in order_reader:
                    ordered_prices = {}
                    orderd_products_id = order["products"]
                    ordered_prices['id'] = order['id']
                    ordered_prices['euros'] = get_total_cost_per_order(product_lst, orderd_products_id)
                    ordered_prices_list.append(ordered_prices)
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(order_path, order_reader.line_num, e))
    except IOError:
        logging.exception('')
    if not len(ordered_prices_list):
        return ValueError('No data available')
    return ordered_prices_list

def calculate_total_cost(number_of_items, cost):
     return (float(number_of_items) * float(cost))

def get_total_cost_per_order(prod_lst, ordered_products_id):
    total_cost = 0.0
    ordered_lst = list(map(int, ordered_products_id.split()))
    ordred_counts = dict()
    if len(ordered_lst)>0:
        for i in ordered_lst:
            ordred_counts[i] = ordred_counts.get(i, 0) + 1
    for  o in ordred_counts:
        for p in prod_lst:
            if int(p['id'])==int(o):
                total_cost+=calculate_total_cost(p["cost"], ordred_counts[o])
                break
    return total_cost

def write_order(ordered_prices_lst):
    header = ordered_prices_lst[0].keys()

    with open(order_prices_path, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, header)
        dict_writer.writeheader()
        dict_writer.writerows(ordered_prices_lst)

def csv_writer(lst, fname):
    header = lst[0].keys()
    with open(fname, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, header)
        dict_writer.writeheader()
        dict_writer.writerows(lst)

def get_products_list(product_pathd):
    # Read entire product file into a list.
    product_list = []
    with open(product_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        product_list = list(reader)
    return product_list
def get_ordered_list(order_path):
        # Read entire product file into a list.
    order_lst = []
    with open(order_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        order_lst = list(reader)
    return order_lst

def get_customers_list():
    # Read entire customer file into a list.
    customer_lst = []
    with open(customers_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        customer_lst = list(reader)
    return customer_lst

def process_customers_purchased_products(order_path, product_path):
    '''
     for each product, gives the list of customers who have purchased this product:
        - id: numeric product id
        - customer_ids: a space-separated list of customer ids of the customers who have purchased this product`
    ''' 
    product_customers_lst = []
    ordered_lst = get_ordered_list(order_path)
    product_lst = get_products_list(product_path)
    for p in product_lst:
        prod_id = p['id']
        product_customers = {}
        customers = []
        for o in ordered_lst:
            os= o['products'].split(' ')
            if str(prod_id) in os:
                # get list of customers who purchased this product ID
                product_customers["id"] = str(prod_id)
                customers.append(o['customer'])
        # make customers id space separated
        customers = ' '.join(customers)
        product_customers["customer_ids"] = customers
        product_customers_lst.append(product_customers)
    return product_customers_lst

def get_customer_ranking(customers_path, order_path, product_path):
    '''
     A customer_ranking.csv containing the following columns, ranked in descending order by total_euros:
     - id: numeric id of the customer
     - firstname: customer first name
     - lastname: customer last name
     - total_euros: total euros this customer has spent on products
    '''
    customer_lst = get_customers_list()
    order_lst = get_ordered_list(order_path)
    product_lst = get_products_list(product_path)
    customer_ranking_lst = []
    for c in customer_lst:
        for o in order_lst:
            customer_ranking = {}
            if c['id'] == o['customer']:
                total_price = get_total_cost_per_order(product_lst, o['products'])
                customer_ranking['id'] = o['customer']
                customer_ranking['firstname'] = c['firstname']
                customer_ranking['lastname'] = c['lastname']
                customer_ranking['total_euros'] = total_price
                customer_ranking_lst.append(customer_ranking)
                break
    # Sort by total_euros in descending order before returning
    return sorted(customer_ranking_lst, key = lambda i: i['total_euros'],reverse=True)

def main():
    parser = argparse.ArgumentParser(description='toolsupplymgt')

    parser.add_argument('-o','--ordered', help='[usage] < python toolsupplymgt.py -o true >  Get ordered products with the total cost of the order', required=True)
    parser.add_argument('-c','--customers', help='[usage] < python toolsupplymgt.py -c true > List customers with all purchased products', required=False)
    parser.add_argument('-r','--ranking', help='[usage] < python toolsupplymgt.py -r true > Get rank of customers total spent on products ', required=False)
    args = vars(parser.parse_args())

    args = parser.parse_args()
    for arg in vars(args):
        if arg == "ordered" and getattr(args, arg):
            # order_prices
            print("Processing order with price")
            ordered_with_total_price = process_order(product_path, order_path)  
            csv_writer(ordered_with_total_price, order_prices_path)
            print("========================\n")

        if arg == "customers" and getattr(args, arg):
            # product_customers
            print("Get customers with all purchased products")
            product_customers_lst = process_customers_purchased_products(order_path, product_path)  
            csv_writer(product_customers_lst, product_customers_path)
            print("========================\n")

        if arg == "ranking" and getattr(args, arg):    
            # # customer_ranking
            print(getattr(args, arg))
            print(arg)
            print("Get rank of customers total spent on products")
            customer_ranking_lst = get_customer_ranking(customers_path, order_path, product_path)  
            csv_writer(customer_ranking_lst, customer_ranking_path)
            print("========================\n")
        

if __name__ == '__main__':
    
    main() 