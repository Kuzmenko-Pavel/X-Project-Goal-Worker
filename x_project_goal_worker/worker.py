import time
from threading import Thread
from uuid import uuid4
import json
from prices import Money

from x_project_goal_worker.logger import logger, exception_message


class Worker(Thread):
    def __init__(self, queue, click_collection, goals_collection, config):
        super(Worker, self).__init__()
        self.__queue = queue
        self.need_exit = False
        self.click_collection = click_collection
        self.goals_collection = goals_collection
        self.config = config
        self.setDaemon(True)
        self.start()

    def run(self):
        logger.info('Starting Worker')
        while True:
            if not self.__queue.empty():
                job = self.__queue.get()
                self.message_processing(*job)
                self.__queue.task_done()
            else:
                if self.need_exit:
                    break
                time.sleep(0.1)
        logger.info('Stopping Worker')

    def message_processing(self, key, data):
        try:
            doc = {}
            d = json.loads(data)
            cid = d.get('cid')
            if cid:
                currency = d.get('currency')
                price = d.get('price')
                click = self.click_collection.find_one({'cid': cid})
                if click:
                    id_account_left = click.get('id_account_left')
                    id_account_right = click.get('id_account_right')
                    id_offer = click.get('id_offer')
                    id_campaign = click.get('id_campaign')
                    id_block = click.get('id_block')
                    id_site = click.get('id_site')
                    if id_account_left and id_account_right and id_offer and id_campaign and id_block and id_site:
                        doc['id_account_left'] = id_account_left
                        doc['id_account_right'] = id_account_right
                        doc['id_offer'] = id_offer
                        doc['id_campaign'] = id_campaign
                        doc['id_block'] = id_block
                        doc['id_site'] = id_site
                        doc['goal'] = 0
                        doc['goal_cost'] = 0
                        doc['goal_auto'] = 1
                        if key == 'goal.manual':
                            doc['goal'] = 1
                            doc['goal_cost'] = price
            if doc:
                self.goals_collection.insert_one(doc)
                print(doc)
            else:
                logger.info('Received message # %s: %s', key, data)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

