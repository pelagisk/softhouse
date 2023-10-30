from contextlib import asynccontextmanager
from fastapi import FastAPI

from .find_best_stocks import find_best_stocks_brute_force
from .watch import create_observer


PATH_TO_INPUT = "in/in.csv"


# `best_stocks` is a global variable which should hold our best 3 stocks
# it is updated using this function
def update_best_stocks():
    # TODO logging
    print("Updating best_stocks")
    global best_stocks    
    best_stocks = find_best_stocks_brute_force(PATH_TO_INPUT)    


# lifespan of FastAPI app is the following
@asynccontextmanager
async def lifespan(app: FastAPI):
    # when starting up:
    # update `best_stocks`   
    update_best_stocks()
    # create an observer which updates it every time the file changes
    observer = create_observer(PATH_TO_INPUT, lambda event: update_best_stocks())
    yield
    # when shutting down: 
    # shut down observer
    observer.stop()
   
# initialize app with that lifespan
app = FastAPI(lifespan=lifespan)

# the only route is a GET
@app.get("/")
def root():
    global best_stocks
    return best_stocks
