# from flask import Flask, render_template, request
# import os
# from dotenv import load_dotenv
# import sqlite3

# from langchain.agents import initialize_agent, Tool
# from langchain.llms import OpenAI

# # Import LangChain tools
# from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
# from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
# from langchain_community.utilities.sql_database import SQLDatabase
# from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
# from langchain_community.tools.arxiv.tool import ArxivQueryRun

# app = Flask(__name__)

# # Load environment variables
# load_dotenv()

# # Ensure OpenAI API key is set
# openai_api_key = os.getenv("OPENAI_API_KEY")
# if not openai_api_key:
#     raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# # Initialize LLM
# llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)

# # Initialize tools
# search_tool = Tool(
#     name="DuckDuckGo Search",
#     func=DuckDuckGoSearchRun().run,
#     description="Use this tool to perform web searches using DuckDuckGo"
# )

# wiki_search_tool = Tool(
#     name="Wikipedia Search",
#     func=WikipediaAPIWrapper().run,
#     description="Use this tool to search Wikipedia for information on any topic."
# )

# # Initialize SQL Database
# db = SQLDatabase.from_uri("sqlite:///example_new.db")
# sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
# sql_tools = sql_toolkit.get_tools()

# arxiv_tool = Tool(
#     name="Arxiv Search",
#     func=ArxivQueryRun().run,
#     description="Use this tool to search academic papers on arXiv. Provide topics, authors, or keywords."
# )

# tools = [search_tool, wiki_search_tool, arxiv_tool] + sql_tools

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent="zero-shot-react-description",
#     verbose=True
# )

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_query = request.form['query']
#         response = agent.run(user_query)
#         return render_template('result.html', query=user_query, response=response)
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)



# app.py

from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Import LangChain tools
from langchain.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper, SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import ArxivAPIWrapper

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Ensure OpenAI API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file.")

# Initialize LLM
llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)

# Initialize tools
search_tool = Tool(
    name="DuckDuckGo Search",
    func=DuckDuckGoSearchAPIWrapper().run,
    description="Use this tool to perform web searches using DuckDuckGo."
)

wiki_search_tool = Tool(
    name="Wikipedia Search",
    func=WikipediaAPIWrapper().run,
    description="Use this tool to search Wikipedia for information on any topic."
)

# Initialize SQL Database
db = SQLDatabase.from_uri("sqlite:///example_new.db")
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = sql_toolkit.get_tools()

arxiv_tool = Tool(
    name="Arxiv Search",
    func=ArxivAPIWrapper().run,
    description="Use this tool to search academic papers on arXiv. Provide topics, authors, or keywords."
)

tools = [search_tool, wiki_search_tool, arxiv_tool] + sql_tools

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.form['query']
        response = agent.run(user_query)
        return render_template('result.html', query=user_query, response=response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)