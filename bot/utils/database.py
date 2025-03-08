from peewee import *

class UserDB(Model):
    user_id = IntegerField(primary_key=True, unique=True)
    agent_id = CharField()

    class Meta:
        database = SqliteDatabase('database.db')
        
def init_db():
    UserDB.create_table(safe=True)
    
def get_agent_id(user_id: int):
    user = UserDB.get_or_none(user_id=user_id)
    if user:
        return user.agent_id
    return None

def store_agent_id(user_id: int, agent_id: str):
    user = UserDB.get_or_none(user_id=user_id)
    if user:
        user.agent_id = agent_id
        user.save()
    else:
        UserDB.create(user_id=user_id, agent_id=agent_id)