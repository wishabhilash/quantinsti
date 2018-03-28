from src.settings import Config
from peewee import *
import uuid

config = Config()

mysql_db = MySQLDatabase(
    config.db['db'],
    user=config.db['user'],
    password=config.db['password']
)


class User(Model):
    name = CharField(unique=True)
    fund = IntegerField(default=0)

    class Meta:
        database = mysql_db    


class Order(Model):
    _id = UUIDField(default=uuid.uuid1())
    user = ForeignKeyField(User, backref='orders')
    instrument = CharField()
    quantity = IntegerField()
    trade_type = CharField()
    buy_price = FloatField(null=True)
    sell_price = FloatField(null=True)
    status = CharField()

    class Meta:
        database = mysql_db
