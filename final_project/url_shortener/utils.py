# This file stores important functions for requests handling


import re

def is_valid_url(url: str) -> bool:
    '''
    A function to validate input full url

            Parameters:
                    url (str): Input full url

            Returns:
                    True - input full URL is URL indeed
                    False - input full URL is not URL  
    '''

    if url is not None:
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return regex.search(url)

    else: 
        return False