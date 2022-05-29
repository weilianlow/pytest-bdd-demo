import json
import uncurl
import requests
from utils.text import sanitise_data


def http_request(**kwargs):
    return requests.request(**kwargs)


def http_curl_request(curl):
    # return only fields that are not empty
    ctx = uncurl.parse_context(curl)
    kwargs = {}
    for field in [[ctx.method, 'method'], [ctx.url, 'url'], [ctx.data, 'data'], [ctx.headers, 'headers'],
                  [ctx.cookies, 'cookies'], [ctx.verify, 'verify'], [ctx.auth, 'auth']]:
        if field[0]:
            kwargs[field[1]] = field[0]
    # omit empty values passed from examples table
    if ctx.data:
        kwargs['data'] = sanitise_data(kwargs['data'])
    return http_request(**kwargs)


def http_response_attribute(response, attribute, expected_value):
    # https://www.w3schools.com/python/ref_requests_response.asp
    dct = {'headers': response.headers == json.loads(expected_value),
           'status code': response.status_code == int(expected_value),
           'text': response.text == expected_value,
           'url': response.url == expected_value}
    return dct.get(attribute, None)



