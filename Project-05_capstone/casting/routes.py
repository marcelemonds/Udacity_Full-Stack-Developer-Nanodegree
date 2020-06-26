from casting import bp
from models import setup_db, Movies, Actors, db
from auth.auth import AuthError, requires_auth
from flask import jsonify, abort, request

# ----------------------------------------------
# GET index
# ----------------------------------------------
@bp.route('/')
def get_index():
    return '''
        <h1>Welcome to the casting agency API<h1>
        <p>Please read the APIs' documentation for neccessary Auth0 roles and permissions, possible endpoints and their request/response data.</p>
        '''

# ----------------------------------------------
# GET Actors
# ----------------------------------------------
@bp.route('/actors')
@requires_auth('get:actors')
def get_actors(payload):
    actors_raw = Actors.query.all()
    actors = [actor.format() for actor in actors_raw]
    return jsonify({
        'success': True,
        'actors': actors
    }), 200


# ----------------------------------------------
# POST Actors
# ----------------------------------------------
@bp.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actors(payload):
    data = request.get_json()
    name = data.get('name', None)
    gender = data.get('gender', None)
    age = data.get('age', None)
    if name is None or gender is None or age is None:
        abort(422)
    try:
        new_actor_check = Actors.query.filter_by(
            name=name,
            gender=gender,
            age=age).one_or_none()
        if new_actor_check:
            abort(422)
        new_actor = Actors(
            name=name,
            gender=gender,
            age=age
        )
        new_actor.insert()
        return jsonify({
            'success': True,
            'actor': new_actor.format()
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# ----------------------------------------------
# PATCH Actors
# ----------------------------------------------
@bp.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(payload, id):
    data = request.get_json()
    if data is None:
        abort(422)
    actor = Actors.query.get(id)
    if actor is None:
        abort(404)
    try:
        if 'name' in data:
            actor.name = data.get('name')
        if 'gender' in data:
            actor.gender = data.get('gender')
        if 'age' in data:
            actor.age = data.get('age')
        actor.update()
        actor = Actors.query.get(id)
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# ----------------------------------------------
# DELETE Actors
# ----------------------------------------------
@bp.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, id):
    actor = Actors.query.get(id)
    if actor is None:
        abort(404)
    try:
        actor.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# ----------------------------------------------
# GET Movies
# ----------------------------------------------
@bp.route('/movies')
@requires_auth('get:movies')
def get_movies(payload):
    movies_raw = Movies.query.all()
    movies = [movie.format() for movie in movies_raw]
    return jsonify({
        'success': True,
        'movies': movies
    }), 200


# ----------------------------------------------
# POST Movies
# ----------------------------------------------
@bp.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies(payload):
    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('release_date', None)
    if title is None or release_date is None:
        abort(422)
    try:
        new_movie_check = Movies.query.filter_by(
            title=title,
            release_date=release_date
            ).one_or_none()
        if new_movie_check:
            abort(422)
        new_movie = Movies(
            title=title,
            release_date=release_date
        )
        new_movie.insert()
        return jsonify({
            'success': True,
            'movie': new_movie.format()
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# ----------------------------------------------
# PATCH Movies
# ----------------------------------------------
@bp.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movies(payload, id):
    data = request.get_json()
    if data is None:
        abort(422)
    movie = Movies.query.get(id)
    if movie is None:
        abort(404)
    try:
        if 'title' in data:
            movie.title = data.get('title')
        if 'release_date' in data:
            movie.release_date = data.get('release_date')
        movie.update()
        movie = Movies.query.get(id)
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# ----------------------------------------------
# DELETE Movies
# ----------------------------------------------
@bp.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, id):
    movie = Movies.query.get(id)
    if movie is None:
        abort(404)
    try:
        movie.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
