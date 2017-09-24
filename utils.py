import traceback

import requests

import bot_logger
from config import url_get_value


def get_coin_value(balance, currency=None, format=2):
    str_format = str("{0:." + str(format) + "f}")

    if not balance > 0:
        return float(0.0)

    try:
        jc_currency = requests.get(url_get_value['coincap']).json()
        coin_val = xpath_get(jc_currency, "/price_usd")
    except:
        try:
            jc_currency = requests.get(url_get_value['cryptocompare']).json()
            coin_val = xpath_get(jc_currency, "/Data/O/Price")
        except:
            traceback.print_exc()
            return 0

    bot_logger.logger.info('value is $%s' % str(coin_val))
    usd_currency = float(str_format.format(int(balance) * float(coin_val)))
    return usd_currency


def check_amount_valid(amount):
    try:
        if (float(amount)) >= 1:
            # print('such amount : '+str(amount))
            return True
        else:
            return False
    except (UnicodeEncodeError, ValueError):
        return False


def xpath_get(mydict, path):
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            try:
                x = int(x)
                elem = elem[x]
            except ValueError:
                elem = elem.get(x)
    except:
        pass

    return elem


def mark_msg_read(reddit, msg):
    unread_messages = [msg]
    reddit.inbox.mark_read(unread_messages)
