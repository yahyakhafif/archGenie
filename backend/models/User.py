import datetime
import bcrypt
import jwt
import os
from config.db import db

user_favorites = db.Table(
    'user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('style_id', db.Integer, db.ForeignKey('styles.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    favorites = db.relationship(
        'Style',
        secondary=user_favorites,
        lazy='dynamic',
        backref=db.backref('favorited_by', lazy='dynamic')
    )

    def set_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )

    def get_signed_jwt_token(self):
        payload = {
            'id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                seconds=int(os.environ.get('JWT_EXPIRE', 86400))
            )
        }
        return jwt.encode(
            payload,
            os.environ.get('JWT_SECRET', 'secret'),
            algorithm='HS256'
        )

    def to_dict(self, include_password=False):
        data = {
            '_id': str(self.id),
            'name': self.name,
            'email': self.email,
            'favorites': [str(s.id) for s in self.favorites.all()],
            'createdAt': self.created_at.isoformat() + 'Z' if self.created_at else None
        }
        if include_password:
            data['password'] = self.password
        return data
