import datetime

from jinja2 import Template
from praw.models import Redditor
from tinydb import TinyDB

import bot_logger
import config
import crypto
import lang
import models
import utils


# buy an reddit gold account for one month
def gold(reddit, msg, tx_queue, failover_time):
    user = models.User(msg.author.name)
    if user.is_registered():
        gold_month = number_gold_credit()

        if msg.body.strip() == 'buy':
            # Number of month
            quantity = 1

            # check if we have enough credits
            if not gold_month >= quantity:
                # store in db want an gold, when bot have new credits a PM can be send
                db = TinyDB(config.DATA_PATH + 'reddit_gold_empty.json')
                db.insert({
                    "user": user.username,
                    "quantity": quantity,
                    'time': datetime.datetime.now().isoformat(),
                })
                db.close()

                msg.reply(Template(lang.message_gold_no_more).render(username=user.username))
                return False

            # check user confirmed balance is ok
            if user.get_balance_confirmed() >= config.price_reddit_gold:
                msg.reply(Template(lang.message_gold_no_enough_pivx).render(username=user.username))
                return False

            # send amount of one month of gold to address
            tx_id = crypto.tip_user(user.address, config.gold_address, config.price_reddit_gold, tx_queue,
                                    failover_time)

            if tx_id:
                # send gold reddit
                Redditor(reddit, user.username).gild(months=quantity)

                # update gold reddit table
                store_user_buy(user, quantity, tx_id)

                # update user history
                models.HistoryStorage.add_to_history(user, sender=user.username, receiver="Reddit",
                                                     amount=config.price_reddit_gold,
                                                     action="buy reddit gold")

                # send succes message
                msg.reply(Template(lang.message_buy_gold_success).render(username=user.username))
            else:
                # send error message
                msg.reply(Template(lang.message_buy_gold_error).render(username=user.username))

        elif msg.body.strip() == 'remind':
            # store in db want an gold, when bot have new credits a PM can be send
            db = TinyDB(config.DATA_PATH + 'reddit_gold_remind.json')
            db.insert({
                "user": user.username,
                "remind": "True",
                'time': datetime.datetime.now().isoformat(),
            })
            db.close()

        else:
            # send info on reddit gold
            msg.reply(Template(lang.message_buy_gold).render(username=user.username, gold_credit=gold_month,
                                                             price=config.price_reddit_gold))
    else:
        bot_logger.logger.info('user %s not registered (command : donate) ' % user.username)
        msg.reply(Template(lang.message_need_register + lang.message_footer).render(username=user.username))


def number_gold_credit():
    credit = 0
    db = TinyDB(config.DATA_PATH + 'reddit_gold.json')
    data = db.all()
    db.close()

    for gold in data:

        if gold['status'] == "buy":
            # user have buy credits
            credit = credit - int(gold['quantity'])

        if gold['status'] == "refill":
            # user have buy credits
            credit = credit + int(gold['quantity'])

    return credit


def store_user_buy(user, quantity, tx_id):
    db = TinyDB(config.DATA_PATH + 'reddit_gold.json')
    db.insert({
        "user_buyer": user.username,
        "quantity": quantity,
        "price": config.price_reddit_gold,
        "currency": 'pivx',
        "amount": config.price_reddit_gold * quantity,
        "usd_price": utils.get_coin_value(1, 'pivx', 8),
        "total_price": utils.get_coin_value(config.price_reddit_gold * quantity, 'pivx', 2),
        'tx_id': tx_id,
        'status': "buy",
        'time': datetime.datetime.now().isoformat(),
    })
    db.close()
