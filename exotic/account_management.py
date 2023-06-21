from exotic.game import Character
from flask_login import UserMixin
from exotic import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String)

    @property
    def characters(self):
        results = Character.query.filter_by(owner=self.id)
        return [c.name for c in results.all()]