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
    _id = UUIDField(default=uuid.uuid1(), primary_key=True)
    user = ForeignKeyField(User, backref='orders')
    instrument = CharField()
    quantity = IntegerField()
    signal = CharField(choices=[(1,'buy'), (2, 'sell')])
    trade_type = CharField(choices=[(1, 'long'), (2, 'short')])
    buy_price = FloatField(null=True)
    sell_price = FloatField(null=True)
    status = CharField(choices=[(1,'open'), (2, 'close')])

    class Meta:
        database = mysql_db
