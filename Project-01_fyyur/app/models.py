from app import db
from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    genres = db.Column(db.String(240))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(240))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    show = db.relationship('Show', backref=db.backref('venue', lazy=True))

    def __repr__(self):
        return f"<id={self.id}, name={self.name}, address={self.city}>"


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(240))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    show = db.relationship('Show', backref=db.backref('artist', lazy=True))

    def __repr__(self):
        return f"<id={self.id}, name={self.name}, address={self.city}>"


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    #creation_date
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<id={self.id}, venue_id={self.venue_id}, artist_id={self.artist_id}, start_time={self.start_time}>"