from datetime import datetime, timedelta
import logging
import pandas as pd

from softhouse.config import DATE_FORMAT


def date_converter(s: str):
    return datetime.strptime(s, DATE_FORMAT)


def find_winners_brute_force(path, n=3):
    """A brute force solution to finding the best stocks"""

    try:
        all_updates = pd.read_csv(path, 
            header=0,  # don't use the provided header
            names=["date", "code", "price"],  # instead use this one
            sep=";", 
            dtype={"code": str, "price": int},
            converters={"date": date_converter},  # convert to date object
            engine="c",  # use the C engine
        )
    except FileNotFoundError:
        logging.warning("Input file not found: returning empty data!")
        return {"winners": []}

    if len(all_updates) == 0:
        logging.warning("Input file is empty: returning empty data!")
        return {"winners": []}        

    #  timedelta representing last 24 hours
    now = all_updates.date.iloc[-1]
    delta = timedelta(days=1)

    # find for all labels the increase in price during last 24 hours
    # save it in the list stock_info
    codes = all_updates.code.unique()
    logging.debug(all_updates)
    logging.debug(f"Stocks to be processed: {codes}")
    stock_info = []
    for code in codes:

        logging.debug(f"Processing stock {code}")
        
        # updates for this stock
        updates = all_updates[all_updates.code == code]

        # latest price
        # (have to convert since FastAPI can't process numpy ints)
        latest_price = int(updates.price.iloc[-1])  

        # all updates before last 24 hours
        updates_before = updates[now - updates.date > delta]

        logging.debug(f"# updates for stock: {len(updates)}")
        logging.debug(f"# updates for stock before 24 hours: {len(updates_before)}")    

        # does the input file contain information about a possible change in stock price?
        if (
            (len(updates) == 1) or                 # not if there is only a single update about the stock
            (len(updates_before) == 0) or          # not if there is no updates before last 24 hours
            (len(updates_before) == len(updates))  # not if there is no updates during last 24 hours
        ):
            # then the stock is assumed to be constant in price during last 24 hours
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


def find_winners_alternative(path, n=3):
    """
    Alternative method of finding winners. 

    The idea is that we can calculate the winners gradually and stop when no stocks can
    improve it.

    I have not checked yet whether this is actually faster!
    Could definitely be slower since it relies on Python and not C. 

    One option is to implement this in e.g. C or Rust.
    """

    from file_read_backwards import FileReadBackwards

    def parse_line(line):
        date_string, code, price_string = line.split(";")
        date = date_converter(date_string)
        price = int(price_string)
        return date, code, price

    lines_read = 0
    prices = dict()    
    percentage_increase = dict()

    candidates = []

    def add_to_candidates(candidate):
        """Adds to candidates in the correct order"""
        percentage = candidate[1]
        for (i, (_, p, _)) in enumerate(reversed(candidates)):
            if percentage <= p: 
                index = len(candidates) - i
                candidates.insert(index, candidate)
                return candidates
        candidates.insert(0, candidate)
        return candidates[0:n]

    #  timedelta representing last 24 hours        
    delta = timedelta(days=1)

    with FileReadBackwards(path) as frb:

        while True:

            line = frb.readline()    
            if not line:
                break

            try: 
                date, code, price = parse_line(line)

                # if we are on the last line, set the current datetime
                if lines_read == 0:
                    now = date            

                # check if the update is older than 24 hours
                is_older = now - date > delta

                # stopping condition
                least_percentage = -1000
                if len(candidates) > 0:
                    least_percentage = candidates[-1][1]
                all_accounted_for = prices.keys() == percentage_increase.keys()
                if (len(candidates) >= n) and (least_percentage >= 0) and all_accounted_for and is_older:
                    break

                # if the code is encountered for the first time
                # and update is within 24 hours
                if not code in prices and (is_older == False): 
                    prices[code] = price
                # and update is older than 24 hours
                elif not code in prices and (is_older == True):    
                    prices[code] = price
                    percentage_increase[code] = 0

                    if (percentage_increase[code] >= least_percentage):
                        candidates = add_to_candidates((
                            code,                            
                            percentage_increase[code],
                            prices[code], 
                        ))

                # if encountered but the percentage has not been calculated yet
                # and the current update is older than 24 hours
                elif (not code in percentage_increase) and (is_older == True):
                    last_price = prices[code]
                    change_in_price = last_price - price                    
                    percentage_increase[code] = 100 * change_in_price / price  

                    if percentage_increase[code] >= least_percentage:
                        candidates = add_to_candidates((
                            code,                            
                            percentage_increase[code],
                            prices[code], 
                        ))

                lines_read += 1

            except ValueError:
                pass

    # return in the specified format
    winners = []
    for i, (name, percent, latest) in enumerate(candidates):
        winners.append({
            "rank": i + 1,
            "name": name,
            "percent": round(percent, 2), 
            "latest": latest,
        })
    return {"winners": winners}