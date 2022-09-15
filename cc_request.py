
import urllib.request
import urllib.error
import json
import sys

def get_from_web(url: str) -> dict or list:
    '''
    Requests JSON formatted data from the API identified by the
    given URL and returns the data as a Python object
    '''
    response = None

    try:
        request = urllib.request.Request(url)

        response = urllib.request.urlopen(request)

    except urllib.error.HTTPError as exception:
        print_web_error_message(exception.getcode(), url, 'NOT 200')

    except (urllib.error.URLError, ValueError):
        print_web_error_message(None, url, 'NETWORK')

    try:
        json_data = response.read().decode(encoding='utf-8')
        data = _convert_data(json_data)
        return data

    except (json.JSONDecodeError, ValueError):
        print_web_error_message(response.getcode(), url, 'FORMAT')

    finally:
        if response:
            response.close()
            
def print_web_error_message(status: int or None, url: str, error: str) -> None:
    '''
    Prints failure message identifying the status of the HTTP request, if applicable,
    and the specific URL and error that caused failure
    '''
    print('FAILED')
    if status is not None:
        print(f'{status} {url}')
    else:
        print(url)
    print(error)
    sys.exit(1)
    
def _convert_data(data: str):
    '''Converts the given JSON formatted data to a Python object'''
    converted_data = json.loads(data)

    # Raises ValueError if json.loads returns an empty object
    if not converted_data:
        raise ValueError
    return converted_data 