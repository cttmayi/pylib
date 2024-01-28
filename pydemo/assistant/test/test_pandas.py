from langchain.agents import create_pandas_dataframe_agent

from langchain.llms import OpenAI
import pandas as pd
 
df = pd.read_csv('titanic.csv')

agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True)

agent.run("how many rows are there?")


