from models import User, db
from werkzeug.security import generate_password_hash

def register_user(email, password, role):
    if not email or not password or not role:
        return None
    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
