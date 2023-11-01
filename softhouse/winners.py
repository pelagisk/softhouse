from datetime import datetime, timedelta
import logging
import pandas as pd
from file_read_backwards import FileReadBackwards

from softhouse.config import DATE_FORMAT


def date_converter(s: str):
    return datetime.strptime(s, DATE_FORMAT)


def find_winners_pandas(path, n=3):
    """A solution using Pandas to finding the best stocks"""

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
        logging.debug(
            f"# updates for stock before 24 hours: {len(updates_before)}"
        )    

        # does the input file contain information about a possible change in 
        # stock price?
        if (
            # not if there is only a single update about the stock
            (len(updates) == 1) or      
            # not if there is no updates before last 24 hours           
            (len(updates_before) == 0) or         
            # not if there is no updates during last 24 hours 
            (len(updates_before) == len(updates))  
        ):
            # then the stock is assumed to be constant in price during last 24 
            # hours
            percentages = 0.0  
        else:  # otherwise, calculate the change
            old_price = updates_before.price.iloc[-1]
            change_in_price = latest_price - old_price
            percentages = 100 * change_in_price / old_price        

        stock_info.append((code, percentages, latest_price))

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


def parse_line(line):
    """
    Parses a line of formmat 'date;code;price' where is of format 
    DATE_FORMAT.
    """
    date_string, code, price_string = line.split(";")
    date = date_converter(date_string)
    price = int(price_string)
    return date, code, price


def find_winners_alternative(path, n=3, assume_update_every_day=False):
    """
    Alternative method of finding winners. Reads file backwards and only
    continues as far as it has to. 

    Should scale with number of updates/day, not number of rows in file.
    Which solution to use depends on the case!

    If it can be assumed that all stocks update every day, we never have to 
    search the entire file and the algorithm runs significantly faster.
    """

    # timedelta representing last 24 hours        
    delta = timedelta(days=1)    

    # from an update (a line), gets the percentage
    get_percentage = lambda update: update['percent']

    # create the candidates as a custom sorted list of max length n
    candidates = []

    # read file from last line backwards:

    lines_read = 0
    prices = dict()       # maps stock codes -> prices
    percentages = dict()  # maps stock codes -> percentages (increase)    

    with FileReadBackwards(path) as frb:

        while True:

            # read lines until EOF (beginning of file :) )
            line = frb.readline()    
            if not line:
                break

            # try to parse the line into an update (date, code, price)
            try:                 
                date, code, price = parse_line(line)
            # continue with next line if this line cannot be parsed
            except ValueError:
                break

            logging.debug(f"Line {lines_read}: {date}, {code}, {price}")

            # when reading the first update (which is assumed to have the 
            # latest date), set the current datetime
            if lines_read == 0:
                now = date            

            # check if the current update is older than 24 hours
            is_older = now - date > delta                

            # whether all encountered stocks/codes also have a percentage
            all_accounted_for = prices.keys() == percentages.keys()

            # the percentage of candidate n in the candidate list
            # (this will be a minimum percentage for the top three)
            min_percentage = -100
            if len(candidates) > n:  # if candidates.len() > n:
                min_percentage = get_percentage(candidates[n-1])

            # stopping conditions, the crucial speed-improvement of this 
            # algorithm:
            # We can stop if these are true, since we are now in the file when 
            # all updates are older than 24 hours. So any unencountered stocks 
            # will have 0% increase. Hence we cannot find any better candidates 
            # if the top n candidates have at least 0% increase.
            # If the top n candidates have < 0% increase, the code will have to
            # read all lines!
            if (
                # we have n candidates (or more)
                (len(candidates) >= n) and  
                # all encountered codes have a percentage calculated
                all_accounted_for and   
                # all candidates have at least 0% increase     
                (min_percentage >= 0) and    
                # the date of the current line is older than 24 hours
                (is_older == True)           
            ):
                break
            # If it can be assumed that all stocks update every day
            # it is enough to assume that we have accounted for all stocks!
            # The algorithm can then stop even if <0% increase since no new
            # stocks can show up in the list
            if (
                (assume_update_every_day == True) and                
                # we have n candidates (or more)
                (len(candidates) >= n) and  
                # all encountered codes have a percentage calculated
                all_accounted_for and    
                # the date of the current line is older than 24 hours
                (is_older == True) 
            ):                
                break

            # if the code is encountered for the first time
            if not code in prices:

                logging.debug(f"    Encountered for first time")

                prices[code] = price                    

                # if update is older than 24 hours
                # calculate percentage
                if is_older == True:  
                    logging.debug("    Already older, percentage: 0")      
                    percentages[code] = 0

                    # add it to candidates if it qualifies
                    logging.debug("    Attempting to insert into candidates")                        
                    candidates.apend(dict(
                        name=code,
                        percent=percentages[code],
                        latest=prices[code],
                    ))  
                    candidates.sort(key=get_percentage, reverse=True)
                    logging.debug("\n".join([
                        f"        {c['name']}: {c['percent']}"
                        for c in candidates
                    ]))   
                                     
            # if encountered but the percentage has not been calculated yet
            # and the current update is older than 24 hours
            elif (not code in percentages) and (is_older == True):                    

                # calculate percentage
                last_price = prices[code]
                change_in_price = last_price - price                    
                percentages[code] = 100 * change_in_price / price 

                logging.debug(f"    Percentage: {percentages[code]}") 

                # add it to candidates if it qualifies
                logging.debug("    Attempting to insert into candidates") 
                candidates.append(dict(
                    name=code,
                    percent=percentages[code],
                    latest=prices[code],
                ))   
                candidates.sort(key=get_percentage, reverse=True)
                logging.debug("\n".join([
                    f"        {c['name']}: {c['percent']}"
                    for c in candidates
                ]))                

            lines_read += 1

    # return in the specified format
    winners = []
    for i, candidate in enumerate(candidates[0:n]):
        winners.append({
            "rank": i + 1,
            "name": candidate["name"],
            "percent": round(candidate["percent"], 2), 
            "latest": candidate["latest"],
        })
    return {"winners": winners}