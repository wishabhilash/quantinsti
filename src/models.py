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
    name = CharField()
    session_key = UUIDField(default=uuid.uuid1())
    fund = IntegerField(default=0)

    class Meta:
        database = mysql_db    


class Order(Model):
    user = ForeignKeyField(User, backref='orders')
    quantity = IntegerField()
    signal = CharField(choices=[(1,'buy'), (2, 'sell')])
    trade_type = CharField(choices=[(1, 'long'), (2, 'short')])
    buy_price = FloatField()
    sell_price = FloatField()
    status = CharField(choices=[(1,'unsettled'), (2, 'settled')])

    class Meta:
        database = mysql_db
