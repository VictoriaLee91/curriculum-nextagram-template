from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Followers(BaseModel):
    fans = pw.ForeignKeyField(User, backref="idols")
    idols = pw.ForeignKeyField(User, backref="fans")
