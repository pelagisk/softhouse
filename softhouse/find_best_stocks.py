from datetime import datetime, timedelta
import pandas as pd


def date_converter(s: str):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def find_best_stocks_brute_force(n=3):
    """A brute force solution to finding the best stocks"""

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

        # all updates before last 24 hours
        updates_before = updates[now - updates.date > delta]

        # if all updates are made before last 24 hours, this condition is true        
        if len(updates_before) == len(df):
            # it follows that no updates were made within 24 hours so the stock has 0% change
            percentage_increase = 0.0               
        else:  # otherwise, calculate the change
            old_price = updates_before.price.iloc[-1]
            change_in_price = latest_price - old_price
            percentage_increase = 100 * change_in_price / old_price        

        stock_info.append((code, percentage_increase, latest_price))

    # sort by index 1: the stock price increase 
    stock_info = sorted(stock_info, key=(lambda line: line[1]), reverse=True)

    # return in the specified format
    winners = []
    for i, (name, percent, latest) in enumerate(stock_info[0:n]):
        winners.append({
            "rank": i + 1,
            "name": name,
            "percent": round(percent, 2), 
            "latest": latest,
        })
    return {"winners": winners}