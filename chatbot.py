# -*- coding: utf-8 -*-

import os
os.environ['OPENAI_API_KEY'] = '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'



#!pip install -q langchain
#!pip install -q openai

import numpy as np
import pandas as pd
import sqlite3


df = pd.read_csv("/Bating_ODI.csv")
df.head()

df.isnull().sum().sum()

df_filled = df.fillna(0)

df[df.isna().any(axis=1)]

df_filled.rename(columns={'Matches_played': 'total_matches', 'Hight_score': 'highest_score','Duck_outs':'ducks'}, inplace=True)

df_filled.columns

conn = sqlite3.connect('ODI_cricket.sqlite')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS batsmen_details (Number int, Player text, Span text, total_matches int, Innings int, Not_outs int, Total_runs_scored int, highest_score int, Average_runs_per_innings float, Balls_faced int, Strike_rate float, Centuries int, Half_centuries int, ducks int)')

conn.commit()



df_filled.to_sql('batsmen_details', conn, if_exists='replace', index = False)



c.execute('''

SELECT Player FROM batsmen_details LIMIT 100

          ''')



for row in c.fetchall():

    print (row)

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

import sqlite3
read_sql_query('SELECT * FROM batsmen_details LIMIT 10;',
               "ODI_cricket.sqlite")

#!pip install langchain-experimental

from langchain_experimental.sql import SQLDatabaseChain

from langchain import OpenAI, SQLDatabase
input_db = SQLDatabase.from_uri('sqlite:///ODI_cricket.sqlite')
llm_1 = OpenAI(temperature=0)

db_agent = SQLDatabaseChain(llm = llm_1,
                            database = input_db,
                            verbose=True)

db_agent.run("Which player has played the most innings?")

db_agent.run("Which player has scored the most centuries?")



"""**Using text UI to generate answers**"""

from langchain_experimental.sql import SQLDatabaseChain
from langchain import OpenAI, SQLDatabase


def execute_sql_query(user_query):
    try:
        result = db_agent.run(user_query)
        return result
    except Exception as e:
        return str(e)

# Load the SQLite database and Langchain/OpenAI components
input_db = SQLDatabase.from_uri('sqlite:///ODI_cricket.sqlite')
llm_1 = OpenAI(temperature=0)
db_agent = SQLDatabaseChain(llm=llm_1, database=input_db, verbose=True)

# Main loop to get user input and display answers
while True:
    user_input = input("Enter a cricket-related question (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    answer = execute_sql_query(user_input)
    print("Answer:", answer)

import re
from langchain_experimental.sql import SQLDatabaseChain
from langchain import OpenAI, SQLDatabase

# Function to execute SQL queries and retrieve the answer
def execute_sql_query(user_query):
    try:
        result = db_agent.run(user_query)
        return result
    except Exception as e:
        return str(e)

input_db = SQLDatabase.from_uri('sqlite:///ODI_cricket.sqlite')
llm_1 = OpenAI(temperature=0)
db_agent = SQLDatabaseChain(llm=llm_1, database=input_db, verbose=True)

answer_pattern = r"Answer:(.+)"

# Main loop to get user input and display answers
while True:
    user_input = input("Enter a cricket-related question (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break

    result = execute_sql_query(user_input)


    result_str = str(result)
    match = re.search(answer_pattern, result_str, re.DOTALL)
    if match:
        print(match.group(1).strip())
        print(result_str)
