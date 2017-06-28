from db import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Binary(), unique=False, nullable=False)
    transformed = db.Column(db.Binary(), unique=False, nullable=True)

    def __repr__(self):
        return '<Image id %r>' % self.id

if __name__ == "__main__":
    db.create_all()
