import mongo_proxy
import pymongo


def get_engine(uri, db):
    safe_conn = mongo_proxy.MongoProxy(pymongo.MongoClient(uri))
    return safe_conn[db]


def get_click_collection(config):
    uri = config['mongo']['uri']
    db = config['mongo']['db']
    collection_name = config['mongo']['collection']['click']
    safe_conn = get_engine(uri, db)
    return safe_conn[collection_name]


def get_goals_collection(config):
    uri = config['mongo']['uri']
    db = config['mongo']['db']
    collection_name = config['mongo']['collection']['goals']
    safe_conn = get_engine(uri, db)
    return safe_conn[collection_name]
