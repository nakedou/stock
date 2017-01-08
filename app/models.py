from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Stock(db.Model):
    __tablename__ = 'stock'

    j_y_s = db.Column(db)
    code = db.Column(db.String(6), nullable=False)
    name = db.Column(db.String(64), nullable=False)


class StockBasics(db.Model):
    __tablename__ = 'stock_basics'

    code = db.Column(db.String(6), nullable=False)
    name = db.Column(db.String(64), nullable=False)


class StockHolder(db.Model):
    __tablename__ = 'stock_holder'

    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(6), nullable=False)
    reg_day = db.Column(db.String(10), nullable=False)
    holders = db.Column(db.Integer, nullable=False)
    change_percent = db.Column(db.Float)
    c_m_j_z = db.Column(db.Float)

