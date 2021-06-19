import csv
import os

header = ['username', 'password']
path = 'accounts.csv'


def add_to_csv(row):
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    f.close()


def is_in_csv(user):
    with open(path, 'r') as f:
        columns = header
        reader = csv.DictReader(f, columns)
        filtered_output = [line for line in reader if line['username'] == user]
        if filtered_output:
                return True


def get_all_users():
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        return [[line[0],":",line[1]] for line in reader]


def add_account(user, password):
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            account=[]
            account.append(user)
            account.append(password)
            writer.writerow(account)
        f.close()


def delete_account(user):
    with open(path, 'r+', newline='') as f:
        columns = header
        reader = csv.DictReader(f, columns)
        filtered_output = [line for line in reader if line['username'] != user]
        f.seek(0)
        writer = csv.DictWriter(f, columns)
        writer.writerows(filtered_output)
        f.truncate()


# with open('employee_birthday.txt') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#             line_count += 1
#     print(f'Processed {line_count} lines.')


if not os.path.exists(path):
    add_to_csv(header)
