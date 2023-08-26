import json
import getPSQLConn as psql
import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

def main():
    sql_select = "SELECT code, content, definitions, content_tokens FROM ca_code;"
    conn = psql.connect()
    rows = psql.select_and_fetch_rows(conn, sql_select)
    df = pd.DataFrame(rows, columns=["Code", "Content", "Definitions", "Content_Tokens"])
    print(df.describe())
    
    df['Num_sentences'] = df.apply(lambda row: row.Content.count("."), axis = 1)
    df['Len_Content'] = df.apply(lambda row: len(row.Content), axis=1)
    plot_histogram_content_tokens(df)
    plot_histogram_num_sentences(df)
    

def plot_histogram_content_tokens(df, cust_range=(0,8500), n_bins=10, useLog=False):
    plt.hist(df["Content_Tokens"], range=cust_range,bins=n_bins, log=useLog)
    plt.xlabel("Tokens in Content")
    plt.ylabel("Number of Rows")
    plt.title("Histogram of Section Size in Tokens")
    plt.show()

def plot_histogram_num_sentences(df, cust_range=(0,150), n_bins=10, useLog=False):
    plt.hist(df["Num_sentences"], range=cust_range, bins=n_bins, log=useLog)
    plt.xlabel("Number of Sentences")
    plt.ylabel("Number of Rows")
    plt.title("Historgram of Sentences in Section")
    plt.show()

    
    
def plot_content_tokens_for_codes():
    pass




if __name__ == "__main__":
    main()