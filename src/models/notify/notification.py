import datetime
import uuid

import src.models.users.controls as users
from src.common.database import Database
from src.common import mail



class Notification(object):
    def __init__(self,creator,action,_event,_id=None,notify=None,time=None,summary=None, read=False):
        self.creator = users.User.get_by_email(creator)
        self.notify = users.User.get_by_email(notify)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.action = action
        self.read = read
        self.time = datetime.datetime.utcnow() if time is None else time
        self.summary = summary[0:40] if summary else summary


    def check(self):
        self.read = True
        self.save_to_db()

    def notify_by_email(self):
        credentials = mail.get_credentials()

        service = mail.discovery.build('gmail', 'v1', http=credentials.authorize(mail.httplib2.Http()))
        Message = mail.CreateMessage('christianthrone@gmail.com', self.notify.email, self.summary,
                                    self.action) #the first email will be whatever the BSG website email would me
        Send = mail.SendMessage(service, self.notify.email, Message)



    def json(self):
        return {
            "read" : self.read,
            "creator": self.creator.email,
            "action": self.action,
            "time" : self.time,
            "summary": self.summary,
            "notify": self.notify.email,
            "_id": self._id
        }
    def __repr__(self):
        return str(self.json())

    def __lt__(self, other):
        return other.time < self.time

    def save_to_db(self):
        Database.update('notifications',{"_id": self._id}, self.json())

    @staticmethod
    def get_by_email(email):
        notifications = []
        for notif in Database.find('notifications', {"notify": email}):
            notifications.append(Notification(**notif))

        notifications.sort()
        return notifications

    @staticmethod
    def get_by_id(_id):
        try:
            notif = Database.find_one('notifications', {"_id": _id})
            return Notification(**notif)
        except Exception:
            return None



    @staticmethod
    def get_read_by_email(email):
        notifications = []
        for notif in Database.find('notifications', {"notify": email}):
            notif = Notification(**notif)
            if not notif.read:
                notifications.append(notif)
        notifications.sort()
        return notifications


            #notif.save_to_db()


if __name__ == "__main__":
    creator = 'chris_ikeokwu@gmail.com'

    event = Event({'Project': "95d3c34f4e91422b9f86e225ec1eae3b"},['test@test.com','test2@test.com','chris_ikeokwu@gmail.com'])


    print(Notification.get_by_email('test@test.com'))
