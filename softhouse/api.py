from contextlib import asynccontextmanager
from fastapi import FastAPI
import datetime
import logging 

from .config import PATH_TO_INPUT, MODE, LOG_FILENAME, STOCKS
from .winners import find_winners_python
from .watch import create_observer


def update_winners():
    """
    `winners` is a global variable which should hold our best 3 stocks. 
    It is updated using this function.
    """
    logging.debug("Updating winners")
    global winners    
    # winners = find_winners_pandas(PATH_TO_INPUT)    
    winners = find_winners_python(PATH_TO_INPUT, stocks=STOCKS) 


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

    update_winners()

    observer = create_observer(PATH_TO_INPUT, lambda event: update_winners())

    yield

    # when shutting down: 

    observer.stop()
   
# initialize app with that lifespan
app = FastAPI(lifespan=lifespan)

# the only route is a GET
@app.get("/")
def root():
    global winners
    return winners
