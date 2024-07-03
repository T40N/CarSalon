from app import db


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    checkup = db.relationship('CheckUp', back_populates='vehicle', uselist=False, cascade="all, delete-orphan")
    rental_date = db.Column(db.Date, nullable=True)
    last_payment_date = db.Column(db.Date, nullable=True)
    total_cost = db.Column(db.Float, nullable=False, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'salon_id': self.salon_id,
            'user_id': self.user_id,
            'checkup': self.checkup.to_dict() if self.checkup else None,
            'rental_date': self.rental_date.isoformat() if self.rental_date else None,
            'last_payment_date': self.last_payment_date.isoformat() if self.last_payment_date else None,
            'total_cost': self.total_cost
        }
