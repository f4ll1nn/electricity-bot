from .settings import MONGO_CONNECT_STRING, IDS, MONGO
import pymongo

class MongoStorage:
    def __init__(self):
        if MONGO:
            self._client = pymongo.MongoClient(MONGO_CONNECT_STRING)
            self._db = self._client['bot']
            self._users = self._db['users']
        else:
            pass

    def get_ids(self):
        if MONGO:
            return [user['user_id'] for user in self._users.find()]
        else:
            return IDS

