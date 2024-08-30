# data_generator.py
import random
import time
import csv
import os
 
def generate_amount():
    if random.random() < 0.05:
        # 5% chance to generate amount between 10 and 1000
        return round(random.uniform(0.0, 10.0), 2)
    elif random.random() < 0.80:
        # 80% chance to generate amount between 1000 and 100000
        return round(random.uniform(10.0, 999.0), 2)
    else:
        # 15% chance to generate amount between 1000 and 100000
        return round(random.uniform(1000.0, 100000.0), 2)
 
 
def generate_transaction(transaction_type):
    if transaction_type == 'bank':
        transaction = {
            'transaction_id': random.randint(1000, 9999),
            'user_id': random.randint(100, 999),
            'amount': generate_amount(),
            'timestamp': time.time(),
            'type': random.choice(['debit', 'credit']),
            'transaction_type': 'bank',
            'account_number': f'AC{random.randint(100000, 999999)}',
            'bank_name': random.choice(['Bank A', 'Bank B', 'Bank C'])
        }
    elif transaction_type == 'ecommerce':
        transaction = {
            'transaction_id': random.randint(1000, 9999),
            'user_id': random.randint(100, 999),
            'amount': generate_amount(),
            'timestamp': time.time(),
            'transaction_type': 'ecommerce',
            'product_id': f'P{random.randint(1000, 9999)}',
            'product_name': random.choice(['Product A', 'Product B', 'Product C']),
            'merchant': random.choice(['Merchant A', 'Merchant B', 'Merchant C'])
        }
    else:
        transaction = {
            'transaction_id': random.randint(1000, 9999),
            'user_id': random.randint(100, 999),
            'amount': generate_amount(),
            'timestamp': time.time(),
            'transaction_type': 'payment_gateway',
            'gateway': random.choice(['Gateway A', 'Gateway B', 'Gateway C']),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'UPI', 'Net Banking'])
        }
   
    return transaction
 
def generate_transactions(transaction_type):
    while True:
        yield generate_transaction(transaction_type)
        time.sleep(1)
 
file_names = {
        'bank': 'Bank_transactions.csv',
        'ecommerce': 'Ecommerce_transactions.csv',
        'payment_gateway': 'Payment_Gateway_transactions.csv'
    }

# Define the columns to be stored
columns = ['transaction_id', 'user_id', 'amount', 'timestamp', 'type', 'is_anomaly']
def store_transaction(transaction_type, transaction, is_anomaly):
    # Check if the file exists
    file_exists = os.path.isfile(file_names[transaction_type])
    # Open the file in append mode
    with open(file_names[transaction_type], mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
       
        # Write the header if the file does not exist
        if not file_exists:
            writer.writeheader()
       
        # Write the transaction data
        writer.writerow({
            'transaction_id': transaction['transaction_id'],
            'user_id': transaction['user_id'],
            'amount': transaction['amount'],
            'timestamp': transaction['timestamp'],
            'type': transaction_type,
            'is_anomaly': is_anomaly
        })