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
         return User(**Database.find("content", {"creator": creator}))
