import datetime
from config.db import db


class FamousExample(db.Model):
    __tablename__ = 'famous_examples'

    id = db.Column(db.Integer, primary_key=True)
    style_id = db.Column(db.Integer, db.ForeignKey('styles.id'), nullable=False)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    architect = db.Column(db.String(255))
    year = db.Column(db.String(50))
    image_url = db.Column(db.Text)

    def to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'architect': self.architect,
            'year': self.year,
            'imageUrl': self.image_url
        }


class Style(db.Model):
    __tablename__ = 'styles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    period = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    characteristics = db.Column(db.ARRAY(db.String), nullable=False, default=[])
    main_features = db.Column(db.ARRAY(db.String), default=[])
    image_url = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    famous_examples = db.relationship(
        'FamousExample',
        backref='style',
        lazy=True,
        cascade='all, delete-orphan'
    )

    creator = db.relationship('User', backref='created_styles', lazy=True)

    def to_dict(self):
        return {
            '_id': str(self.id),
            'name': self.name,
            'period': self.period,
            'description': self.description,
            'characteristics': self.characteristics or [],
            'mainFeatures': self.main_features or [],
            'famousExamples': [ex.to_dict() for ex in self.famous_examples],
            'imageUrl': self.image_url,
            'createdBy': str(self.created_by),
            'createdAt': self.created_at.isoformat() + 'Z' if self.created_at else None
        }
