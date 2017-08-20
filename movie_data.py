"""API to fetch and massage data from themoviedatabase.org
"""
import sys
import requests


API = 'https://api.themoviedb.org/3/'
# not really a good idea to save the key here but for simplification
# let's ignore it
API_KEY = '9d0ca632dc2b2f950b258b3721bc0948'

def request_json(req):
    """
    Utility function
    shortcut to request data in json format, exceptions caught by caller
    """
    return requests.get(req).json()


def reraise_with_info(info, e):
    """
    add additional info and reraise exceptions
    """
    raise type(e), type(e)('{}, when: {}'.format(e.message, info)), sys.exc_info()[2]

def get_configuration():
    """
    Utility function
    fetch configurations used to build full TMDB image url
    """
    req = '{}configuration?api_key={}'.format(API, API_KEY)

    try:
        data = request_json(req)
        return {
            'base_url': data['images']['base_url'],
            'size': 'w500'
        }
    except Exception as e:
        reraise_with_info('getting configuration from TMDB', e)

CONFIGURATION = get_configuration()

def get_movies_data():
    """
    1. Fetch data from "now playing" movie list from themoviedatabase.org
    2. Transform data to agreed interface containing:
        - title
        - poster_image_url
        - trailer_youtube_url
    3. Drop any movie that missed any of the above info

    Returns:
        list of dicts: containing movie data
    """
    req = '{}movie/now_playing?api_key={}'.format(API, API_KEY)

    try:
        movies = request_json(req)['results']
        movies = map(transform_data, movies)
        return filter(bool, movies)
    except Exception as e:
        reraise_with_info('getting now-playing movies from TMDB', e)

def transform_data(tmdb_movie):
    """
    Transform data from raw json to ready to use dict data

    Returns:
        either:
            - dict: contains title, poster_image_url and trailer_youtube_url
            - None: if any of the above info missing
    """
    try:
        return {
            'title': tmdb_movie['title'],
            'poster_image_url': build_poster_url(tmdb_movie['poster_path']),
            'trailer_youtube_url': get_youtube_url(tmdb_movie['id'])
        }
    except:
        print u'Ignored movie [{}] due to insufficient data'.format(tmdb_movie['title'])
        return None

def build_poster_url(poster_path):
    """
    since fetched movie data returns a partial path to the poster
    we need to build the full one according to:
    https://developers.themoviedb.org/3/configuration/get-api-configuration
    """
    return CONFIGURATION['base_url'] + CONFIGURATION['size'] + poster_path

def get_youtube_url(movie_id):
    """
    build full url to the movie trailer on youtube
    """
    def build_youtube_url(youtube_video_id):
        return 'https://www.youtube.com/watch?v={}'.format(youtube_video_id)

    def is_youtube_trailer(video):
        return video['type'] == 'Trailer' and video['site'] == 'YouTube'

    req = '{}movie/{}/videos?api_key={}'.format(API, movie_id, API_KEY)

    try:
        videos = request_json(req)['results']
        trailer = next(v for v in videos if is_youtube_trailer(v))
        return build_youtube_url(trailer['key'])
    except Exception as e:
        reraise_with_info('getting youtube trailer url of movie with id {}'.format(movie_id), e)
