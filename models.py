from peewee import *
from peeweedbevolve import * 
from  config import config

db = SqliteDatabase('db1.db')

db = MySQLDatabase(
    config.db_name,
    user=config.user,
    password=config.password,
    host = 'localhost'
)

class BaseModel(Model):
    class Meta:
        database = db
    evolve = False

class User(BaseModel):
    id = AutoField()
    username = CharField()
    password = CharField()
    name = CharField()
    email = CharField()
    role = CharField()
    status = BooleanField()
    img = CharField()

class Lang(BaseModel):
    id = AutoField()
    title = CharField()
    thumbnail = CharField()
    slug = CharField()
    status = BooleanField()

class Slider(BaseModel):
    id = AutoField()
    name = CharField(max_length=100)
    img = CharField(max_length=256)
    lang_id = ForeignKeyField(Lang, related_name="sliders",)

class Advantage(BaseModel):
    id= AutoField()
    title = CharField(max_length=255)
    icon = CharField(max_length=255)
    des = TextField()
    lang_id = ForeignKeyField(Lang, related_name="advantages",)

class SectionThree(BaseModel):
    id = AutoField()
    img  = CharField(max_length=255)
    title = CharField(max_length=255)
    des = TextField()
    lang_id = ForeignKeyField(Lang, related_name='sectionthrees')

class SectionFour(BaseModel):
    id =AutoField()
    title = CharField(max_length=255)
    img = CharField(max_length=255)
    des = TextField()
    youtube_button_text = CharField(max_length=20)
    text_advantage =  TextField()
    text_button = CharField(max_length=20)
    lang_id = ForeignKeyField(Lang, related_name="sectionfours")


 
class Infrastructure(BaseModel):
    id = AutoField()
    title = CharField(max_length=200)
    img = CharField(max_length=255)
    des = TextField()
    lang_id = ForeignKeyField(Lang, related_name="infrastructure")


class Gallery(BaseModel):
    id  = AutoField()
    img = CharField(max_length=255)
    

class CallToAction(BaseModel):
    id = AutoField()
    title = CharField(max_length=255)
    des = TextField()
    text_button = CharField(max_length=20)
    lang_id = ForeignKeyField(Lang, related_name="calltoactions")

class Contact(BaseModel):
    id = AutoField()
    title = CharField(max_length=200)
    des = TextField()
    address = CharField(max_length=255)
    phone = CharField(max_length=20)
    email = CharField(max_length=70)
    text_button = CharField(max_length=30)
    longitude = CharField(max_length=50)
    latitude = CharField(max_length=50)
    lang_id = ForeignKeyField(Lang, related_name="contacts")


class Residence(BaseModel):
    id = AutoField()
    name = CharField(max_length=255)
    img = CharField(max_length=255)
    lang_id  = ForeignKeyField(Lang, related_name="Residences")


class Block(BaseModel):
    id = AutoField()
    name = CharField(max_length=255)
    img = CharField(max_length=255)
    residence = ForeignKeyField(Lang, related_name = "residences")
    lang_id  = ForeignKeyField(Lang, related_name = "blocks")

class Layout(BaseModel):
    id = AutoField()
    title = CharField(max_length=255)
    floor = CharField(max_length=20)
    square = CharField(max_length=30)
    img = CharField(max_length=200)


class Ids(BaseModel):
	id = AutoField()
	img = IntegerField()
    



if __name__ == '__main__':
    db.evolve()
    Ids(img = 1).save()
	