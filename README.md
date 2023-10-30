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
- Input can be modified while running
- Output: JSON
    - list of three
    - fields:
        - rank: int
        - name: string - the code of the stock
        - percent: float %.2f - the price increase during last 24 in percent (select the three stocks of largest percentual increase during the day)
        - latest: int - latest price


# Approximation level 0

- [x] Read CSV input file using pandas
- [x] Query using pandas
- [x] FastAPI, return JSON
- [x] Save the winners in a variable that is updated by a service

# TODOs

- [ ] Logging
- [ ] API testing
- [ ] Profiling - find bottlenecks

# Installation

For dependency management, install [Python Poetry](https://python-poetry.org) through

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then to install dependencies, from the project root run

```bash
poetry install
```

# Usage

On localhost, run

```bash
poetry run uvicorn softhouse:app
```