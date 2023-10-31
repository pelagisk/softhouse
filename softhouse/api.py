from contextlib import asynccontextmanager
from fastapi import FastAPI
import datetime
import logging 

from .config import PATH_TO_INPUT, MODE, LOG_FILENAME
from .find_best_stocks import find_best_stocks_brute_force
from .watch import create_observer


def update_best_stocks():
    """
    `best_stocks` is a global variable which should hold our best 3 stocks. 
    It is updated using this function.
    """
    logging.debug("Updating best_stocks")
    global best_stocks    
    best_stocks = find_best_stocks_brute_force(PATH_TO_INPUT)    


# lifespan of FastAPI app is the following
@asynccontextmanager
async def lifespan(app: FastAPI):

    # when starting up:

    if MODE == "debug":
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(
        filename=LOG_FILENAME, 
        level=level,
        filemode='w', 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    update_best_stocks()

    observer = create_observer(PATH_TO_INPUT, lambda event: update_best_stocks())

    yield

    # when shutting down: 

    observer.stop()
   
# initialize app with that lifespan
app = FastAPI(lifespan=lifespan)

# the only route is a GET
@app.get("/")
def root():
    global best_stocks
    return best_stocks
