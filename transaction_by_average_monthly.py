import requests
from datetime import datetime

# response = requests.get(end_point)
# print(f"status code: {response.status_code}")
# json = response.json()
# print(f"the content: {json['page'], len(json['data'])}")
#
# pages = json['total_pages']
# print(pages)

# for i in range(pages - 1):
#     response = requests.get(end_point)
#     json = response.json()
#     print(f"the page number: {json['page'], json['per_page']}")


def getUserTransaction(uid, txnType, monthYear):
    end_point = 'https://jsonmock.hackerrank.com/api/transactions/search?'

    ep = end_point + f'userId={uid}&txnType={txnType}'
    response = requests.get(ep)
    json = response.json()

    data: list = json['data']
    for page in range(2, json['total_pages']+1):
        response = requests.get(ep + f'&page={page}')
        json = response.json()
        data.extend(json['data'])

    filtered = []
    tally = 0
    for item in data:

        timestamp = item['timestamp']
        month_year = datetime.utcfromtimestamp(timestamp//1000).strftime('%m-%Y')

        if month_year == monthYear:
            amount = float(''.join(ch for ch in item['amount'] if ch.isdigit() or ch == '.'))
            tally += amount
            item['amount'] = amount
            filtered.append(item)

    average = tally / len(filtered) if len(filtered) > 0 else 0

    transactions = []
    for item in filtered:
        if item['amount'] > average:
            transactions.append(item['id'])

    transactions.sort()
    return transactions if len(transactions) > 0 else [-1]


if __name__ == '__main__':
    trans = getUserTransaction(4, 'debit', '02-2019')
    print(trans)
