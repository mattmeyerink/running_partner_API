"""Contains the db model for a runs."""
from app import db
from datetime import datetime as dt


class Run(db.Model):
    """Represents a run in the db."""
    __tablename__ = "runs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'))
    distance = db.Column(db.Float)
    date = db.Column(db.String(50))
    notes = db.Column(db.String())
    run_city = db.Column(db.String(50))
    run_state = db.Column(db.String(10))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    
    def __repr__(self):
        return f"<Run {self.user_id}: {self.date} | {self.distance}>"

    def save(self):
        """Save a run to the db."""
        db.session.add(self)
        db.session.commit()

    def remove(self):
        """Delete the run from the db."""
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
        """Create a run from a dictionary."""
        for field in ["user_id", "distance", "date", "notes", "run_city", "run_state"]:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        """Output a dictionary from a run object."""
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "distance": self.distance,
            "date": self.date,
            "notes": self.notes,
            "run_city": self.run_city,
            "run_state": self.run_state,
            "created_on": self.created_on
        }
        return data
