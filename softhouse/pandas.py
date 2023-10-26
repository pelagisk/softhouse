from datetime import datetime
import pandas as pd

def date_converter(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

df = pd.read_csv("in.csv", 
    header=0,  # don't use the provided header
    names=["date", "code", "price"],  # instead use this one
    sep=";", 
    converters={"date": date_converter}  # convert to date object
)

print(df)