from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), unique=True, nullable=False)

    salon = db.relationship("Salon", back_populates="address")

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'salon_id': self.salon_id
        }
