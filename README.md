# Installation

To install, create a virtual environment and install dependencies. 

```bash
python3.8 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

All commands below are assumed to be run inside this virtualenv. 

Note: developed with Python 3.8 for compatibility. It seems to work also for 
Python 3.11.


# Usage

```bash
uvicorn softhouse:app
```


# Testing

Run `pytest` with

```bash
py.test
```


# Profiling

Profile the code using `cProfile` with

```bash
python profiling/run.py > profiling/profile.txt
```


# Scaling test of the two methods

We can compare the two solution methods by running

```bash
python profiling/benchmark.py
```