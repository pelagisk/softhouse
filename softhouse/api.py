from fastapi import FastAPI
from .find_best_stocks import find_best_stocks_brute_force


app = FastAPI()


@app.get("/")
def root():  # async def    
    winners = find_best_stocks_brute_force()
    return winners