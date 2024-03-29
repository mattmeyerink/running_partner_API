from app import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """Class to represent a user in the database"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    active_plan = db.Column(db.Integer)
    runs = db.relationship('Run', cascade='all, delete-orphan', backref='users', lazy=True)
    custom_plans = db.relationship('CustomPlan', cascade='all, delete-orphan', backref='users', lazy=True)

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def save(self):
        """Save the current user to the db."""
        db.session.add(self)
        db.session.commit()

    def remove(self):
        """Delete the current user from the db."""
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
        """Create a new user object from a dict."""
        for field in ["first_name", "last_name", "username", 
                "email", "city", "state", "active_plan"]:
            if field in data:
                setattr(self, field, data[field])
    
    def to_dict(self):
        """Returns a dictionary with user information."""
        data = {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "city": self.city,
            "state": self.state,
            "active_plan": self.active_plan
        }
        return data

    def hash_password(self, original_password):
        """Hashes the input password so it can be stored in the db safely."""
        self.password = generate_password_hash(original_password)

    def check_hashed_password(self, input_password):
        """Determine if the input password is the same as the saved password."""
        return check_password_hash(self.password, input_password)
    
    