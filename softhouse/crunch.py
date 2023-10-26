from datetime import datetime, timedelta
import pandas as pd


# first attempt, brute force solution


def date_converter(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


df = pd.read_csv("in.csv", 
    header=0,  # don't use the provided header
    names=["date", "code", "price"],  # instead use this one
    sep=";", 
    converters={"date": date_converter},  # convert to date object
)

# find for all labels the increase in price during last 24 hours
now = df.date.iloc[-1]
delta = timedelta(days=1)

codes = df.code.unique()
stock_info = []

for code in codes:
    # updates for this stock
    updates = df[df.code == code]

    # latest price
    latest_price = updates.price.iloc[-1]

    # all updates within last 24 hours
    updates_last_day = updates[now - updates.date < delta]
    updates_before = updates[now - updates.date > delta]

    # if it is not updated during the last day, it is constant
    if len(updates_last_day) == 0:
        percentage_increase = 0.0               
    else:  # otherwise, calculate the change
        old_price = updates_before.price.iloc[-1]
        change_in_price = latest_price - old_price
        percentage_increase = 100 * change_in_price / old_price        

    stock_info.append((code, percentage_increase, latest_price))

stock_info = sorted(stock_info, key=(lambda line: line[1]), reverse=True)
print(stock_info[0:3])