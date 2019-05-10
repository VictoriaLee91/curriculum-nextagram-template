from models.base_model import BaseModel
from models.user import User
from flask_login import LoginManager
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import AWS_LINK


class Images(BaseModel):
    user_image = pw.CharField(
        null=True, default=None)
    user = pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def image_url(self):
        return f'{AWS_LINK}/{self.user_image}'

    @hybrid_property
    def total_payments(self):
        from models.payments import Payments
        total_payments = Payments.select(
            fn.SUM(Payments.amount)).where(Payments.image_id == self.id)
