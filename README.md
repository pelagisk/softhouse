# Specification

- REST API
- Input: CSV file
    - which can be updated at any time (~5 mins)
    - size limited to a few hundred rows
    - contains any update of share prices
    - 0, 1 or more updates for each share every day is possible
    - current datetime is considered to be the last day in list
        - current day or current dayetime?
    - sorted in descending datetime order
    - delimiter: ;
    - columns: 
        - Datum: datetime - the time at which the update was sent
        - Kod: string - code/name of the stock
        - Kurs: int - stock price

- Output: JSON
    - list of three
    - fields:
        - rank: int
        - name: string - the code of the stock
        - percent: float %.2f - the price increase during last 24 in percent (select the three stocks of largest percentual increase during the day)
        - latest: int - latest price


# Approximation level 0

- Detect when file is updated
- Read CSV input file using pandas
- Query using pandas
- Return as JSON

# Ideas
- FastAPI
- Pandas
- os.stat
- watchdog
- https://file-read-backwards.readthedocs.io/en/latest/readme.html