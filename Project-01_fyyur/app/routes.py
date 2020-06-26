#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from app import app, db
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
import logging
from logging import Formatter, FileHandler
from sqlalchemy import or_
from flask_wtf import Form
from app.forms import *
from app.models import *
import datetime

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  latest_artists = Artist.query.order_by(Artist.creation_date).limit(10).all()
  latest_venues = Venue.query.order_by(Venue.creation_date).limit(10).all()
  
  return render_template('pages/home.html', latest_artists=latest_artists, latest_venues=latest_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  areas = Venue.query.distinct(Venue.city, Venue.state).all()
  data = [dict(city=area.city, 
                state=area.state, 
                venues=[dict(id=venue.id, 
                              name=venue.name
                              ) for venue in Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()]
                	) for area in areas]

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(or_(
    Venue.name.ilike(f'%{search_term}%'),
    Venue.city.ilike(f'%{search_term}%'),
    Venue.state.ilike(f'%{search_term}%')
    )).all()

  return render_template('pages/search_venues.html', results=results, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  venue = Venue.query.get(venue_id)
  upcoming_shows = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>=datetime_now).all()
  past_shows = db.session.query(Show, Artist).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<=datetime_now).all()
  
  return render_template('pages/show_venue.html', venue=venue, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  try:
    form = request.form
    venue = Venue(
      name=form['name'],
      city=form['city'],
      state=form['state'],
      address=form['address'],
      phone=form['phone'],
      genres=request.form.getlist('genres'),
      seeking_talent=bool(form['seeking_talent']),
      seeking_description=form['seeking_description'],
      facebook_link=form['facebook_link'],
      website=form['website'],
      image_link=form['image_link']
    )
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  # TODO: modify data to be the data object returned from db insertion
  if error:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
  finally:
    db.session.close()
  if error:
    flash('An error ocurred. Venue ' + request.form['name'] + ' could not be deleted.')
  else:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully deleted!')
  return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()

  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(or_(
    Artist.name.ilike(f'%{search_term}%'),
    Artist.city.ilike(f'%{search_term}%'),
    Artist.state.ilike(f'%{search_term}%')
    )).all()

  return render_template('pages/search_artists.html', results=results, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  artist = Artist.query.get(artist_id)
  upcoming_shows = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>=datetime_now).all()
  past_shows = db.session.query(Show, Venue).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<=datetime_now).all()
  
  return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    form = request.form
    artist = Artist.query.get(artist_id)
    artist.name = form['name']
    artist.city = form['city']
    artist.state = form['state']
    artist.phone = form['phone']
    artist.genres = request.form.getlist('genres')
    artist.seeking_venue = bool(form.get('seeking_venue'))
    artist.seeking_description = form['seeking_description']
    artist.facebook_link = form['facebook_link']
    artist.website = form['website']
    artist.image_link = form['image_link']
    
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True 
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + form['name'] + ' could not be updated.')
  else:
    flash('Artist ' + form['name'] + ' was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    form = request.form
    venue = Venue.query.get(venue_id)
    venue.name = form['name']
    venue.city = form['city']
    venue.state = form['state']
    venue.address = form['address']
    venue.phone = form['phone']
    venue.genres = form.getlist('genres')
    venue.seeking_talent = bool(form.get('seeking_talent'))
    venue.seeking_description = form['seeking_description']
    venue.facebook_link = form['facebook_link']
    venue.website = form['website']
    venue.image_link = form['image_link']
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True 
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + form['name'] + ' could not be updated.')
  else:
    flash('Venue ' + form['name'] + ' was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  try:
    form = request.form
    artist = Artist(
      name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      phone=request.form['phone'],
      genres=request.form.getlist('genres'),
      seeking_venue=bool(form['seeking_venue']),
      seeking_description=form['seeking_description'],
      facebook_link=request.form['facebook_link'],
      website=request.form['website'],
      image_link=request.form['image_link']
    )
    db.session.add(artist)
    db.session.commit()
  except:
      error = True
      print(sys.exc_info())
      db.session.rollback()
  finally:
      db.session.close()
  if error:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  else:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(Show, Artist, Venue).join(Artist).join(Venue)

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    form = request.form
    show = Show(
      artist_id=int(form['artist_id']),
      venue_id=int(form['venue_id']),
      start_time=datetime.datetime.strptime(form['start_time'], '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True 
  finally:
    db.session.close()
  if error:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()
'''
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
