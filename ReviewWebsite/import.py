import MySQLdb
import json
from decouple import config

db = MySQLdb.connect(host=config('HOST'), user=config('DB_USER'), 
    password=config('DB_PASS'), database=config('DATABASE'))


def main():
    print("Select an option.")
    print("You can find the data in: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv")
    print("1. Import movie data")
    selection = 0
    while selection == 0:
        try:
            selection = int(input())
        except ValueError:
            print("Invalid option.")
    
    match selection:
        case 1:
            ImportMovies()

def ImportMovies():
    has_file = False
    while not has_file:
        try:
            directory = input("What is the directory of the csv files?\n")
            data = open(directory+"/movies_metadata.csv", 'r', encoding='utf-8')
            has_file = True
        except FileNotFoundError:
            print("This directory does not exist")
    
    debug = input("Would you like to see the data? (Y/N)")
    if debug == "Y":
        i = 0
        for line in data:
            print(line)
    split = input("Decode the data? (Y/N)\n")
    rows = []
    if (split == "Y"):
        for line in data:
            row = []
            L=0
            for i in range(len(line)):
                if (line[i] == ','):
                    row.append(line[L:i])
                    L=i+1
                if (line[i] == '"'):
                    i+=1
                    L=i
                    while(line[i] != '"'):
                        i+=1
                    row.append(line[L:i])
            row.append(line[L:])
            rows.append(row)
        
        check = input("Check decoded data? (Y/N)\n")
        if (input == "Y"):
            for row in rows:
                print(rows[1])
    else:
        return
    insert = input("Insert the data? (Y/N)\n")
    if insert == "Y":
        for line in data:
            print(line)
    

if __name__ == "__main__":
    main()