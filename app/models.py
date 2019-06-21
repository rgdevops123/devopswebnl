from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import LargeBinary, Column, Integer, String

from app import db, login_manager, logger


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary)
    phone = Column(String)
    mobile = Column(String)
    department = Column(String)
    company = Column(String)
    location = Column(String)
    title = Column(String)

    @classmethod
    def is_user_name_taken(cls, username):
        q = db.session.query(User).filter(User.username == username)
        return db.session.query(q.exists()).scalar()

    @classmethod
    def is_email_taken(cls, email):
        q = db.session.query(User).filter(User.email == email)
        return db.session.query(q.exists()).scalar()

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            logger.debug("ERROR {}.".format(e))
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()
