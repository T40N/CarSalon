from app import db


class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    vehicles = db.relationship('Vehicle', backref='salon', lazy=True)
    address = db.relationship('Address', back_populates='salon', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vehicles': [vehicle.to_dict() for vehicle in self.vehicles],
            'address': self.address.to_dict() if self.address else None
        }