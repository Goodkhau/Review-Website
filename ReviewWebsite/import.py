import MySQLdb
import json
from decouple import config
from datetime import datetime

db = MySQLdb.connect(host=config('HOST'), user=config('DB_USER'), 
    password=config('DB_PASS'), database=config('DATABASE'))
cur = db.cursor()


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
    
    debug = input("Would you like to see the data? (Y/N)\n")
    if debug == "Y":
        i = 0
        for line in data:
            print(line)
            i+=1
            if i >= 10:
                break
    
    split = input("Decode the data? (Y/N)\n")
    rows = []
    if (split == "Y"):
        for line in data:
            rows.append(parseline(line))
        rows.pop(0)
        
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
        error_count = 0
        accepted_count = 0
        for row in rows:
            try:
                if row[16] == '':
                    row[16] = 0
                row[14] = datetime.strptime(row[14], '%Y-%m-%d').date()
                cur.execute("INSERT INTO myreviews_movie (movie_id, title, description, release_date, runtime, " \
                "date_added, number_reviews, poster, total_score, director_id, average_score) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (row[5], row[8], row[9], row[14], row[16], datetime.now(), 0, "fallback.png", 0, None, None)
                )
                accepted_count+=1
            except:
                error_count+=1
                print("Error for: ", end="")
                print(row)
        print("There were " + str(error_count) + " errors and " + str(accepted_count) + " accepted.")

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
            try:
                while line[i] != '"' or line[i+1] != ',' or line[i-1] == '"':
                    i+=1
                    if i >= len(line):
                        i-=1
                        break
            except IndexError:
                print("Error for (likely newlines in the description):")
                print(line)
                SystemExit
            row.append(line[L:i])
            i+=1
            L=i+1
        i+=1
    row.append(line[L:])
    return row

if __name__ == "__main__":
    main()