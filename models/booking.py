from app import db
from models.users import User
from models.courses import Course

class Booking(db.Document):
    meta = {'collection': 'booking'}
    name = db.ReferenceField(User)
    courseName = db.ReferenceField(Course)
    tee_time = db.ListField()