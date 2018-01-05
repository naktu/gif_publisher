import logging
import requests


logging.getLogger(__name__).addHandler(logging.NullHandler)


def get_page(url, params):
    """
    :param url: url
    :param timeout: timeout
    :return: response if return code 200 or fail
    """

    result = {}
    exception_happened = True
    try:
        resp = requests.get(url, params=params)
    except Exception as e:
        logging.error('{}'.format(e))
    else:
        if resp.status_code != 200:
            logging.error('Http code not 200: {}'.format(resp.status_code))
        else:
            exception_happened = False
            result['result'] = 'ok'
            result['data'] = resp
    finally:
        if exception_happened:
            result['result'] = 'fail'
            logging.info('Function get_page params {}'.format(url))
    return result
