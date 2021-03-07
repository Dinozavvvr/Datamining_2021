import datetime


class Post:

    def __init__(self, text=None, date=None, owner_id=None):
        self.text = text
        self.date = date
        self.owner_id = owner_id

    def print(self):
        print(
            "date = {date}\nowner = {owner_id}\ntext = {text}".format(date=self.date,
                                                                      owner_id=self.owner_id,
                                                                      text=self.text))
