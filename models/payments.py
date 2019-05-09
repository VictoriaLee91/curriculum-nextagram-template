from models.base_model import BaseModel
from models.user import User
from models.images import Images
import peewee as pw'


class Payments(BaseModel):
    user = pw.ForeignKeyField(User, backref='payments')
    image = pw.ForeignKeyField(User, backref='payments')
    amount = pw.DecimalField(null=False)
