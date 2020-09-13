from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(
        db.String(250),
        nullable=False)
    src = db.Column(
        db.String(2000),
        nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "src": self.src
        }

    def __str__(self):
        return f"src {self.src}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @ classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @ classmethod
    def get_all(cls, user_id):
        return cls.query.filter_by(user_id).all()
