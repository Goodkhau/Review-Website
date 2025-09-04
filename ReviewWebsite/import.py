import MySQLdb
from decouple import config

db = MySQLdb.connect(host=config('HOST'), user=config('DB_USER'), 
    password=config('DB_PASS'), database=config('DATABASE'))


def main():
    print("Select an option.")
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
            directory = input()
            data = open(directory+"/movies_metadata.csv", 'r')
            has_file = True
        except FileNotFoundError:
            print("This directory does not exist")
    
    debug = input("Would you like to see the data? (Y/N)")
    if debug == "Y":
        for line in data:
            print(line)

if __name__ == "__main__":
    main()