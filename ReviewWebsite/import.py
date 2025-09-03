import MySQLdb
from decouple import config

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
            