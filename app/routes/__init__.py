from .salon_routes import salon_bp
from .vehicle_routes import vehicle_bp
from .user_routes import user_bp
from .check_up_routes import checkup_bp
from .address_routes import address_bp


def register_routes(app):
    app.register_blueprint(salon_bp, url_prefix='/api/salons')
    app.register_blueprint(vehicle_bp, url_prefix='/api/vehicles')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(checkup_bp, url_prefix='/api/checkups')
    app.register_blueprint(address_bp, url_prefix='/api/address')
