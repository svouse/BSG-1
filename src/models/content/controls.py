from src.common.database import Database
import uuid

class Content:
    def __init__(self,name,creator,attributes,_id=None): # attributes is a dict where i dont really know what's inside
        self.name = name
        self.attributes = attributes
        self._id = uuid.uuid4().hex if _id is None else _id
        self.creator = creator


    def json(self):
        return {
        "name": self.name
        "_id": self._id
        "creator": self.creator
        "attributes": self.attributes
        }

    @staticmethod
    def get_by_creator(creator):
         Database.initialize()
         return Content(**Database.find("content", {"creator": creator}))


    @staticmethod
    def get_by_id(_id):
         Database.initialize()
         return Content(**Database.find_one("content", {"_id": _id}))

    @staticmethod
    def get_by_name(name):
         Database.initialize()
         return Content(**Database.find("content", {"name": name}))
