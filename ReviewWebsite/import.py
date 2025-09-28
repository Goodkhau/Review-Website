import MySQLdb
import json
import sys
from decouple import config
from datetime import datetime

db = MySQLdb.connect(host=config('HOST'), user=config('DB_USER'), 
    password=config('DB_PASS'), database=config('DATABASE'))
cur = db.cursor()

error_count = 0
accepted_count = 0
auto_increment = 1


def main():
    print("Select an option.")
    print("You can find the data in: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv")
    print("1. Import movie data")
    print("2. Import movie_genre_list")
    selection = 0
    while selection == 0:
        try:
            selection = int(input())
        except ValueError:
            print("Invalid option.")
    
    match selection:
        case 1:
            ImportMovies()
        case 2:
            importGenreMovieRelation()
    
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
    global error_count, accepted_count
    insert = input("Insert the data? (Y/N)\n")
    if insert == "Y":
        debug = input("Would you like to see the errors? (Y/N)\n")
        for row in rows:
            specificQuery(type, row, qry_str, debug)
        print("There were " + str(error_count) + " errors and " + str(accepted_count) + " accepted.")

def specificQuery(type, row, qry_str, debug):
    global error_count, accepted_count, auto_increment
    match type:
        case "movie_data":
            try:
                if row[16] == '':
                    row[16] = 0
                row[14] = datetime.strptime(row[14], '%Y-%m-%d').date()
                cur.execute(qry_str, (row[8], "", "fallback.png", None, 0, 0, row[14], row[16], datetime.now(), datetime.now()))
                accepted_count+=1
            except:
                error_count+=1
                if (debug == 'Y'):
                    print("Error for: ", end="")
                    print(row)
        case "genre":
            try:
                row[3] = row[3].replace("'", '"')
                JSON = json.loads(row[3])
                for element in JSON:
                    cur.execute("SELECT * FROM myreviews_genre WHERE name = %s", (element["name"],))
                    if cur.fetchone() == None:
                        cur.execute("INSERT INTO myreviews_genre (name, description) VALUES (%s, %s)", (element["name"], ""))
                accepted_count+=1
            except:
                error_count+=1
                print("Error for: ", end="")
                print(row)
        case "movie_genre":
            try:
                cur.execute("SELECT * FROM myreviews_movie WHERE title = %s", (row[8],))
                q = cur.fetchone()
                if q == None:
                    cur.fetchall()
                    print(row[8] + " is not in the database")
                    return
                cur.fetchall()
                row[3] = row[3].replace("'", '"')
                JSON = json.loads(row[3])
                for element in JSON:
                    cur.execute("SELECT * FROM myreviews_genre WHERE name = %s", (element["name"],))
                    if cur.fetchone() == None:
                        cur.fetchall()
                        continue
                    cur.fetchall()
                    cur.execute(qry_str, (q[0], element["name"]))
            except:
                error_count+=1
                print("Error for: ", end="")
                print(row)


def commitPrompt():
    commit = input("Commit the queries? (Y/N)\n")
    if commit == 'Y':
        db.commit()
    else:
        return
    cur.close()
    db.close()
    sys.exit()

def importGenreMovieRelation():
    data = openFile("/movies_metadata.csv")
    debugData(data)
    rows = decodeMovieMetaData(data)
    generateQueryStr(
        "INSERT INTO myreviews_movie_genre_list (movie_id, genre_id) VALUES (%s, %s)",
        rows,
        "genre"
    )
    commitPrompt()
    generateQueryStr(
        "INSERT INTO myreviews_movie_genre_list (movie_id, genre_id) VALUES (%s, %s)",
        rows,
        "movie_genre"
    )
    commitPrompt()

def ImportMovies():
    data = openFile("/movies_metadata.csv")
    debugData(data)
    rows = decodeMovieMetaData(data)
    generateQueryStr(
        "INSERT INTO myreviews_movie (title, description, poster, average_score, total_score, number_reviews, " \
        "release_date, runtime, date_added, modified_at) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        rows,
        "movie_data"
    )
    commitPrompt()

if __name__ == "__main__":
    main()