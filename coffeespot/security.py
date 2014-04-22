from models.tables import DBSession, Users

from sqlalchemy.orm.exc import NoResultFound

from passlib.hash import bcrypt

def group_from_user(username, request):
    try:
        users_db = DBSession.query(Users)
        return [users_db.filter(Users.name == username).first().group]
    except:
        return []

def verify_password(username, password):
    try:
        user_password = \
            DBSession.query(Users)\
            .filter(Users.name == username)\
            .first()\
            .password
        return bcrypt.verify(password, user_password)
    except:
        return False
