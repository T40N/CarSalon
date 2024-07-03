from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    vehicles = db.relationship('Vehicle', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vehicles': [vehicle.to_dict() for vehicle in self.vehicles]
        }
