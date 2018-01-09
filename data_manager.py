import csv


def read_csv(filename):
    with open(filename, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]


def write_csv(filename, new_data):
    with open(filename, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in new_data:
            writer.writerow(row)
