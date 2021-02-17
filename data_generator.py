import csv
import random

with open('dataset_train.csv', mode='w', newline='') as csv_file:
    fieldnames = ['label', 'ft1', 'ft2', 'ft3']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(1000):
        writer.writerow({'label': random.randint(0,1), 'ft1': random.randint(0, 10), \
            'ft2': random.randint(0, 10), 'ft3': random.randint(0,10)})
