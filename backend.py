# # from langchain_groq import ChatGroq
# # from dotenv import load_dotenv

# # load_dotenv()

# # llm = ChatGroq(
# #     model="llama-3.3-70b-versatile"
# # )

# # print(llm)

# # result = llm.invoke("What is the capital of India?")
# # print(result.content)

# import boto3
# import json
# client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# # print(client.meta.service_model.operation_model("AgenticRetrieveStream").input_shape)
# # AgenticRetrieveStream (streaming, agent-driven multi-step retrieval)
# response = client.agentic_retrieve_stream(
#     messages=[{'content': {'text': 'How much percentage of saving i have done.'}, 'role': 'user'}],
#     retrievers=[{
#         'configuration': {'knowledgeBase': {'knowledgeBaseId': 'AGB4OZY3M2'}}
#     }],
#     agenticRetrieveConfiguration={
#         'foundationModelType': 'MANAGED',
#         'rerankingModelType': 'MANAGED',
#         'maxAgentIteration': 5
#     }
# )
# for event in response['stream']:
#     if 'result' in event:
#         for item in event['result'].get('results', []):
#             print("Result:")
#     elif 'traceEvent' in event:
#         attrs = event['traceEvent']['attributes']
#         print(f"Trace")
# # Retrieve
# response = client.retrieve(
#     knowledgeBaseId='AGB4OZY3M2',
#     retrievalQuery={'text': 'How much percentage of saving i have done.'}
# )
# print("Retrieve:", response['retrievalResults'])



# retrieval_results = response["retrievalResults"]


# # Your existing Bedrock Agent Runtime client
# # client = boto3.client(
# #     "bedrock-agent-runtime",
# #     region_name="us-east-1"
# # )

# # Bedrock Runtime client for the LLM
# llm_client = boto3.client(
#     "bedrock-runtime",
#     region_name="us-east-1"
# )

# # Extract text from retrieved documents
# context = "\n\n".join(
#     result["content"]["text"]
#     for result in retrieval_results
# )

# print("Retrieved Context:")
# print(context)
# question = "How much percentage of saving I have done?"


# # --------------------------------
# # 2. Create Prompt
# # --------------------------------

# prompt = f"""
# You are a helpful financial assistant.

# Answer the user's question using ONLY the information
# provided in the context.

# You can perform simple arithmetic calculations when required.

# Do not make up any information.

# If the required information is not present in the context,
# say:
# "I don't have enough information in the provided documents."

# Context:
# ----------------
# {context}
# ----------------

# User Question:
# {question}

# Give a concise and direct answer.
# """


# # --------------------------------
# # 3. Invoke Gemma 3 27B PT
# # --------------------------------

# model_id = "google.gemma-3-27b-it"
# response = llm_client.invoke_model(
#     modelId=model_id,
#     body=json.dumps({
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "text": prompt
#                     }
#                 ]
#             }
#         ],
#         "max_tokens": 512,
#         "temperature": 0.1
#     }),
#     contentType="application/json",
#     accept="application/json"
# )

# response_body = json.loads(response["body"].read())

# print(response_body)


import boto3
import json
# --------------------------------
# 1. Create clients
# --------------------------------

client = boto3.client(
    "bedrock-agent-runtime",
    region_name="us-east-1"
)

llm_client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

# --------------------------------
# 2. User question
# --------------------------------

# question = "How much percentage of saving I have done?"
question = "How much overall  I have earn in year 2023-24?"

# --------------------------------
# 3. Retrieve from Knowledge Base
# --------------------------------

response = client.retrieve(
    knowledgeBaseId="AGB4OZY3M2",
    retrievalQuery={
        "text": question
    }
)

retrieval_results = response["retrievalResults"]


# --------------------------------
# 4. Extract retrieved text
# --------------------------------

context = "\n\n".join(
    result["content"]["text"]
    for result in retrieval_results
)

print("Retrieved Context:")
print(context)


# --------------------------------
# 5. Create prompt
# --------------------------------

prompt = f"""
You are a helpful financial assistant.

Answer the user's question using ONLY the information
provided in the context.

You can perform simple arithmetic calculations when required.

Do not make up any information.

If the required information is not present in the context,
say:
"I don't have enough information in the provided documents."

Context:
----------------
{context}
----------------

User Question:
{question}

Give a concise and direct answer.
"""


# --------------------------------
# 6. Invoke Gemma
# --------------------------------

model_id = "google.gemma-3-27b-it"

response = llm_client.invoke_model(
    modelId=model_id,
    body=json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 512,
        "temperature": 0.1
    }),
    contentType="application/json",
    accept="application/json"
)


# --------------------------------
# 7. Read response
# --------------------------------

response_body = json.loads(
    response["body"].read()
)

print("LLM Response:")
print(response_body)