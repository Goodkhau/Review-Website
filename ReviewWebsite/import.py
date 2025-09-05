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
            rows.append(parseline(line))
        
        check = input("Check decoded data? (Y/N)\n")
        if (check == "Y"):
            c = 0
            for row in rows:
                for i in range(len(row)):
                    print(str(i) + ": " + row[i])
                c+=1
                if (c==4):
                    break
    else:
        return

    insert = input("Insert the data? (Y/N)\n")
    if insert == "Y":
        for line in data:
            print(line)

def parseline(line):
    row = []
    L=0
    i=0
    while i < len(line):
        if (line[i] == ','):
            row.append(line[L:i])
            L=i+1
        if (line[i] == '"'):
            i+=1
            L=i
            while line[i] != '"':
                i+=1
                if i >= len(line):
                    i-=1
                    break
            row.append(line[L:i])
            i+=1
            L=i+1
        i+=1
    row.append(line[L:])
    return row

if __name__ == "__main__":
    main()