#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import parse, request, error
from socket import timeout
import logging
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('/var/log/zabbix/telegram.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(message, subject):
    global result

    proxy = 'http://name:password@ip:port'

    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

    token = 'token'
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    params = parse.urlencode({"chat_id": -000, "text": message})
    params = params.encode('utf-8')

    try:

        logger.info('Subject = %s, MESSAGE = %s', subject, message)
        result = request.urlopen(url, params).read()
        logger.info('RESULT = %s', result)

    except error.HTTPError as e:
        logger.info('HTTP ERROR = %s', e)
    except error.URLError as e:
        logger.info('URL ERROR = %s', e)
    except Exception as e:
        logger.info('Exception = %s', e, result)
    except timeout:
        logger.info('socket timed out - URL %s', url)
    else:
        logger.info('Access successful.')


if __name__ == "__main__":
    subj = sys.argv[1]
    message_list = []
    message_string = None

    for text_item in range(3, len(sys.argv)):
        message_list.append(sys.argv[text_item])

    message_string = ' '.join(str(element) for element in message_list)
    send_message(message_string, subj)
