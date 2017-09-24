import os
import time
import traceback
from Queue import Queue
from multiprocessing import Value
from threading import Thread

import bot_logger
import config
import crypto
from pivxtipbot import pivxtipbot

if __name__ == "__main__":
    bot_logger.logger.info("Bot Started !!")

    # get wallet pass phrase from user input
    crypto.init_passphrase()

    # check passphase is good
    crypto.check_passphrase()

    while True:
        try:
            # create directory to store user history
            if not os.path.exists(config.history_path):
                os.makedirs(config.history_path)

            # start bot
            tx_queue = Queue()
            failover_time = Value('i', 0)

            Bot = pivxtipbot()

            # thread to process reddit commands
            thread_master = Thread(name='app', target=Bot.main, args=(tx_queue, failover_time,))
            # thread to process pending tips
            thread_pending_tip = Thread(name='pending_tip', target=Bot.process_pending_tip,
                                        args=(tx_queue, failover_time,))
            # some security thread
            thread_anti_spamming_tx = Thread(name='anti_spam', target=Bot.anti_spamming_tx)

            thread_double_spend_check = Thread(name='double_spend_check',
                                               target=Bot.double_spend_check,
                                               args=(tx_queue, failover_time,))

            thread_double_spend_check = Thread(name='vanitygen',
                                               target=Bot.vanitygen,
                                               args=(tx_queue, failover_time,))

            thread_master.start()
            thread_pending_tip.start()
            thread_anti_spamming_tx.start()
            thread_double_spend_check.start()

            thread_master.join()
            thread_pending_tip.join()
            thread_anti_spamming_tx.join()
            thread_double_spend_check.join()

            bot_logger.logger.error('All bot task finished ...')
        except:
            traceback.print_exc()
            bot_logger.logger.error('Resuming in 30sec...')
            time.sleep(30)
