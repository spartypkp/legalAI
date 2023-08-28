import json

def main():
    pass

def read_all_test_queries():
    with open("testQueries.txt") as queries_file:
        text = queries_file.read()
    list_of_queries = queries_file.split(",")
    return list_of_queries



if __name__ == "__main__":
    main()