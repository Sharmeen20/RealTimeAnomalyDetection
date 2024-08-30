# kafka_producer.py
from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'), api_version=(0, 10, 1))

def generate_transaction():
    transaction = {
        'transaction_id': random.randint(1000, 9999),
        'user_id': random.randint(100, 999),
        'amount': round(random.uniform(10.0, 1000.0), 2),
        'timestamp': time.time(),
        'type': random.choice(['debit', 'credit'])
    }
    return transaction

while True:
    transaction = generate_transaction()
    producer.send('transactions', transaction)
    time.sleep(1)



