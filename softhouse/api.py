from contextlib import asynccontextmanager
from fastapi import FastAPI
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



from .find_best_stocks import find_best_stocks_brute_force
from .event import create_observer


global winners 
winners = find_best_stocks_brute_force() 

def update_winners():
    # TODO logging
    print("Updating winners")
    global winners    
    winners = find_best_stocks_brute_force()    

observer = create_observer("in.csv", lambda event: update_winners())

@asynccontextmanager
async def lifespan(app: FastAPI):
    update_winners()
    yield
    observer.stop()
   
app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return winners
