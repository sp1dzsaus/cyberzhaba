from datetime import datetime

from app.db.models import SqlMembership
from app.entities.users import User
from app.entities.guilds import Guild
from app.db import database


class Membership:
    def __init__(self, user_id, guild_id):
        self.user_id = user_id
        self.guild_id = guild_id

        # this ensures these actually exist -
        # avoiding foreign key errors!
        self.user = User(user_id)
        self.guild = Guild(guild_id)

        db_sess = database.session()
        sql_membership = db_sess.query(SqlMembership).filter(
            SqlMembership.user == user_id, SqlMembership.guild == guild_id
        ).first()
        if not sql_membership:
            sql_membership = SqlMembership(user=user_id, guild=guild_id)
            db_sess.add(sql_membership)
            db_sess.commit()

        self.id = sql_membership.id

    def __bool__(self):
        # is this necessary?
        return True

    def sql(self) -> SqlMembership:
        return database.session().get(SqlMembership, self.id)

    @property
    def karma(self):
        return self.sql().karma

    def add_karma(self, amount):
        db_sess = database.session()
        membership = db_sess.get(SqlMembership, self.id)
        membership.karma += amount
        db_sess.commit()

    def mark_activity(self, activity_type: str):
        db_sess = database.session()
        membership = db_sess.get(SqlMembership, self.id)
        membership.last_activity = datetime.now()
        membership.last_activity_type = activity_type
        db_sess.commit()

    def set_birthday_event_id(self, eid: int):
        db_sess = database.session()
        membership = db_sess.get(SqlMembership, self.id)
        membership.birthday_event_id = eid
        db_sess.commit()
