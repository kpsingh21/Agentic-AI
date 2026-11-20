from tavily import TavilyClient
import os
from dotenv import load_dotenv


load_dotenv()

client = TavilyClient(
    api_key= os.getenv("TAVILY_API_KEY")
)


response = client.search(
    query="what is the top most hotel in udaipur",
    search_depth="advanced",
    max_results=1
)
# print(response)
# print(type(response))

# all_keys = response.keys()

# print(response['results']) 

# def tavilSearch(query):
#     responses = client.search(
#     query= query,
#     search_depth="advanced",
#     max_results=1
#     )

#    return responses

def tavilSearch(query):
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=1
    )
    return response



