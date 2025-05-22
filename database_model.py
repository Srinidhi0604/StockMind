from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password_hash = db.Column(db.String(200), nullable = False)
    def set_passsword(self, passw):
        self.password_hash = generate_password_hash(passw)
    def check_password(self, passw):
        return check_password_hash(self.password_hash, passw)
    def get_passw_hash(self):
        return self.password_hash
    