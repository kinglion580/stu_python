from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, UserMixin):
    __table__ = 'user'
    
    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY 

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class Company(Base):
    __table__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=True)
    logo = db.Column(db.String(64), nullable=False)
    site = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(24), nullable=False)
    location = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(100))
    about = db.Column(db.String(1024))
    tags = db.Column(db.String(128))
    stack = db.Column(db.String(128))
    team_introduction = db.Column(db.String(256))
    welfares = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', userlist=False, backref=db.backref('company', userlist=False))

    def __repr__(self):
        return '<Company {}>'.format(self.name)


    
