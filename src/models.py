from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=False, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'published': self.published
        }
