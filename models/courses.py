from app import db
from models.hole import Hole

#Below is for TMA
class HoleUploadInfo(db.Document):
    index = db.ListField(db.StringField())
    par = db.ListField(db.StringField())
    dist = db.ListField(db.StringField())
#Above is for TMA

class Course(db.Document):
    meta = {'collection': 'course'}
    name = db.StringField()
    #TMA
    #holesDetail = db.ReferenceField(HoleUploadInfo)
    #ECA
    holesDetail = db.ListField(db.ReferenceField(Hole))

    image = db.URLField()
    description = db.StringField()