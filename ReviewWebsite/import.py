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
    
def openFile(fileDir):
    has_file = False
    while not has_file:
        try:
            directory = input("What is the directory of the csv files?\n")
            data = open(directory+fileDir, 'r', encoding='utf-8')
            has_file = True
            return data
        except FileNotFoundError:
            print("This directory does not exist")

def debugData(data):
    debug = input("Would you like to see the data? (Y/N)\n")
    if debug == "Y":
        i = 0
        for line in data:
            print(line)
            i+=1
            if i >= 10:
                break

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

def decodeMovieMetaData(data):
    split = input("Decode the data? (Y/N) Will exit program if N.\n")
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
    return rows

def generateQueryStr(qry_str, rows, type):
    insert = input("Insert the data? (Y/N)\n")
    if insert == "Y":
        debug = input("Would you like to see the errors? (Y/N)\n")
        error_count = 0
        accepted_count = 0
        for row in rows:
            specificQuery(type, row, qry_str, debug)
        print("There were " + str(error_count) + " errors and " + str(accepted_count) + " accepted.")

def specificQuery(type, row, qry_str, debug):
    match type:
        case "movie_data":
            try:
                if row[16] == '':
                    row[16] = 0
                row[14] = datetime.strptime(row[14], '%Y-%m-%d').date()
                cur.execute(qry_str, (row[5], row[8], row[9], row[14], row[16], 
                                      datetime.now(), 0, "fallback.png", 0, None, None))
                accepted_count+=1
            except:
                error_count+=1
                if (debug == 'Y'):
                    print("Error for: ", end="")
                    print(row)
        case "genre_movie":
            try:
                ## ParseJson
                ## Check if genre is in db, insert if not
                ## Regardless of last if, insert genre movie into genre_movie_list
                cur.execute(qry_str,) ## Input values from row, likely row 3 genre and 8 title
                accepted_count+=1
            except:
                error_count+=1
                if (debug == 'Y'):
                    print("Error for: ", end="")
                    print(row)

def commitPrompt():
    commit = input("Commit the queries? (Y/N)\n")
    if commit == 'Y':
        cur.commit()
    cur.close()

def importGenreMovieRelation():
    data = openFile("/movies_metadata.csv")
    debugData(data)
    rows = decodeMovieMetaData(data)
    generateQueryStr(
        "INSERT INTO myreviews_", ## Complete query str.
        rows,
        "genre_movie"
    )
    commitPrompt()

def ImportMovies():
    data = openFile("/movies_metadata.csv")
    debugData(data)
    rows = decodeMovieMetaData(data)
    generateQueryStr(
        "INSERT INTO myreviews_movie (movie_id, title, description, release_date, runtime, " \
        "date_added, number_reviews, poster, total_score, director_id, average_score) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        rows,
        "movie_data"
    )

if __name__ == "__main__":
    main()