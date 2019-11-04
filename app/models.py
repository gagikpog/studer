from datetime import datetime
from app import db
from app.utility.utility import get_hash_password

class mixin():
    def to_dict(self):
        res = {}
        di = self.__dict__
        j = 0
        for i in di:
            if j == 0:
                j+=1
                continue
            res[str(i)] = getattr(self, i)
        return res

    def init_of_dict(self, _dict):
        for key, val in _dict.items():
            setattr(self, key, val)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )

class User(db.Model, mixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    phone = db.Column(db.String(32), index=True, unique=True)
    mail = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    sname = db.Column(db.String(64))
    pname = db.Column(db.String(64))
    born = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    activity = db.Column(db.String(64))
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref= db.backref('users', lazy='dynamic'))
    bills = db.relationship('Bill', backref='author', lazy='dynamic') #отношения с таблицей Bill
    bills = db.relationship('Bill', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, {}>'.format(self.name, self.mail)

    def set_password(self, password):
        pass_hash = get_hash_password(password)
        self.password_hash = pass_hash


class Bill(db.Model, mixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(64))
    deadline = db.Column(db.DateTime)
    summ = db.Column(db.Integer)
    description = db.Column(db.String(512))
    category = db.Column(db.Integer)
    status = db.Column(db.String(32))
    views = db.Column(db.Integer)

    client = db.Column(db.Integer, db.ForeignKey('user.id'))
    # student = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Bill {}>'.format(self.title)

class Role(db.Model,mixin):
    id = db.Column(db.Integer(), primary_key=True)
    status_authorization = db.Column(db.String(15))
