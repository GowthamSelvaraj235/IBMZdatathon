import pandas as pd


def clean_csv(filepath, expected_fields=128):
    cleaned_rows = []
    
    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file, 1):
            fields = line.strip().split(',')
            if len(fields) == expected_fields:
                cleaned_rows.append(fields)
            else:
                print(f"Skipping line {line_num}: Expected {expected_fields} fields, but got {len(fields)}")
    
    
    with open('cleaned_gesture_data.csv', 'w') as f:
        for row in cleaned_rows:
            f.write(','.join(row) + '\n')


clean_csv('gesture_data3.csv')


data = pd.read_csv('cleaned_gesture_data.csv')
