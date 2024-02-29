from typing import List
from promptflow import tool
import urllib.request
import json
import os
import ssl
import datetime
import pandas as pd 
import time 
import sys
from ast import literal_eval
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


@tool
def semantickernel(question: str, context: str):
    """
    This tool aggregates the processed result of all lines to the variant level and log metric for each variant.

    :param processed_results: List of the output of line_process node.
    :param variant_ids: List of variant ids that can be used to group the results by variant.
    :param line_numbers: List of line numbers of the variants. If provided, this can be used to
                        group the results by line number.
    """

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data = f"'chat_history':{context}, 'question':{question}"
    # data = {"messages": [{"role": "system","content": "You are an AI assistant that helps people find information." }  ],  "temperature": 0.7,  "top_p": 0.95,  "frequency_penalty": 0,"presence_penalty": 0,  "max_tokens": 800}
    body = str.encode(json.dumps(data))
    # body = data 
    # body = str.encode("hello")

    print(body, file=sys.stderr)
    url = "http://localhost:7071/QnA"

    # Replace this with the primary/secondary key or AMLToken for the endpoint
    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'accept': 'text/plain', 'Content-Type':'text/plain' }
    req2 = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req2)

        result = response.read()
        
        # cananswer3=" ".join(line.strip() for line in cananswer.splitlines())        
        # print("\n Thought: ", result['output']['thought'])
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))     
        result = "The request failed with status code: " + str(error.code)
    return result    


