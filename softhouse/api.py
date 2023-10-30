from contextlib import asynccontextmanager
from fastapi import FastAPI
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .find_best_stocks import find_best_stocks_brute_force
from .watch import create_observer

# `best_stocks` is a global variable which should hold our best 3 stocks
global best_stocks 

# it is updated using this function
def update_best_stocks():
    # TODO logging
    print("Updating best_stocks")
    global best_stocks    
    best_stocks = find_best_stocks_brute_force()    

# input file `in.csv` is watched for changes
observer = create_observer("in.csv", lambda event: update_best_stocks())

# lifespan of FastAPI app is the following
@asynccontextmanager
async def lifespan(app: FastAPI):
    # when starting up, update `best_stocks`
    update_best_stocks()
    yield
    # when shutting down, remember to shut down observer
    observer.stop()
   
# initialize app with that lifespan
app = FastAPI(lifespan=lifespan)

# the only route is a GET
@app.get("/")
def root():
    return best_stocks
