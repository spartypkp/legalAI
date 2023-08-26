import json
import getPSQLConn as psql
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

def main():
    sql_select = "SELECT code, content, definitions, content_tokens FROM ca_code WHERE code='BPC';"
    conn = psql.connect()
    rows = psql.select_and_fetch_rows(conn, sql_select)
    df = pd.DataFrame(rows, columns=["Code", "Content", "Definitions", "Content_Tokens"])
    print(df.head())
    
    df['Num_sentences'] = df.apply(lambda row: row.Content.count("."), axis = 1)
    df['Len_Content'] = df.apply(lambda row: len(row.Content), axis=1)
    plot_histogram_content_tokens(df)
    

def plot_histogram_content_tokens(df):
    plt.hist(df["Content_Tokens"])
    plt.xlabel("Tokens in Content")
    plt.ylabel("Number of Rows")
    plt.title("Histogram of Section Size in Tokens")
    plt.show()

def plot_histogram_num_sentences(df):
    plt.hist(df["Num_sentences"])
    plt.xlabel("Number of Sentences")
    plt.ylabel("Number of Rows")
    plt.title("Historgram of Sentences in Section")
    plt.show()
    
def plot_content_tokens_for_codes():
    pass




if __name__ == "__main__":
    main()