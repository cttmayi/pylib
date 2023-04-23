#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os 
from pprint import pprint
import requests

import os

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
endpoint = 'https://api.bing.microsoft.com/v7.0/search' # os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/search"

def bing_search(query):
# Construct a request
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt }
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        val = response.json().get('webPages').get('value')

        ret = []
        for v in val:
            ret.append(v['url'])

    except Exception as ex:
        raise ex

    return ret



if __name__ == '__main__':
    # Query term(s) to search for. 
    query = "Microsoft Cognitive Services"
    ret = bing_search(query)
    pprint(ret)
