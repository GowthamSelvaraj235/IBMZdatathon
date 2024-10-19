import pandas as pd


chunk_size = 100  
try:
    for chunk in pd.read_csv('gesture_dat6.csv', chunksize=chunk_size):
        print(chunk)
except pd.errors.ParserError as e:
    print(f"Error processing CSV: {e}")
