from app import db

class Hole(db.Document):
    meta = {'collection': 'hole'}
    index = db.IntField()
    dist = db.IntField()
    par = db.IntField()