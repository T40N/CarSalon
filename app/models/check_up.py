from app import db


class CheckUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_checkup_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), unique=True, nullable=False)

    vehicle = db.relationship("Vehicle", back_populates="checkup")

    def to_dict(self):
        return {
            'id': self.id,
            'last_checkup_date': self.last_checkup_date.isoformat(),
            'notes': self.notes,
            'vehicle_id': self.vehicle_id
        }
