import requests
from datetime import datetime


def get_user_transaction(uid, txnType, monthYear):

    # create define URL with search query
    end_point = 'https://jsonmock.hackerrank.com/api/transactions/search?'
    ep = end_point + f'userId={uid}&txnType={txnType}'  # <-- search query is appended to the endpoint

    # use request module to perform the network call
    response = requests.get(ep)

    # get the json object from the network response object
    # the json object is a dictionary of key value pairs where
    # the values can be anything like strings, numbers or arrays
    json = response.json()

    # since the network API returns pages of the requested
    # data we need to request any additional data matching
    # the URL query above by appending a page number as an
    # additional URL query parameter: page=2 for example
    data: list = json['data']
    for page in range(2, json['total_pages'] + 1):
        # this is where we append a different page number
        # to get any additional pages that matches our
        # URL query
        response = requests.get(ep + f'&page={page}')
        json = response.json()
        # as we get additional data items we extend
        # our list of already gotten data items that
        # was defined outside this for loop
        data.extend(json['data'])

    # since the URL query does not support a monthYear parameter
    # we are forced to look at each of the records for this user
    # and compare the timestamp with the provided monthYear function
    # parameter; if a match is found the we add the item to the
    # filtered list, otherwise we just ignore it.
    filtered = []
    tally = 0  # <-- we use this as a helper for computing the average of the amount per use record/item
    for item in data:

        # since this timestamp is the number of milliseconds since 1970 we need
        # to extract the month and year in order to be able to make the comparision
        # between a user's record/item timestamp and the monthYear parameter value
        # that was passed to this function
        timestamp = item['timestamp']
        month_year = datetime.utcfromtimestamp(timestamp // 1000).strftime('%m-%Y')

        if month_year == monthYear:
            # this the amount stored in a record is in a string
            # format of the type: $1,200.89, we must strip all
            # characters that are not digits or decimal points
            # like so: $1,200.89 --> 1200.89 and cast it to a float
            amount = float(''.join(ch for ch in item['amount'] if ch.isdigit() or ch == '.'))

            # we modify the original record only locally to store the
            # the amount value as float because we will use this later
            # to compute the average amount. That is, we replace:
            #       item['amount'] = $1,200.89, with
            #       item['amount'] = 1200.89
            tally += amount
            item['amount'] = amount

            filtered.append(item)

    # compute average amount
    average = tally / len(filtered) if len(filtered) > 0 else 0

    # the final filtering of the records/items occurs here.
    # the requirements stated that only transactions that
    # are greater than the average amount be returned.
    transactions = []
    for item in filtered:
        if item['amount'] > average:
            transactions.append(item['id'])

    # the final requirement is that the transactions be filtered
    transactions.sort()
    return transactions if len(transactions) > 0 else [-1]


if __name__ == '__main__':
    trans = get_user_transaction(4, 'debit', '02-2019')
    print(trans)
