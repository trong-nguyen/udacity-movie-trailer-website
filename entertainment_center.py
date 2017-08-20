"""Main file that:
	- Fetch movie data from an API (TMDB)
	- Instantiate Movie instances
	- Render webpages using fetched data
	- Open page in default browser
"""

from fresh_tomatoes import open_movies_page
from media import Movie
from movie_data import get_movies_data

def render():
	"""
	render movie data into fresh_tomatoes.html
	open webpage
	"""
	movies = [Movie(data) for data in get_movies_data()]
	open_movies_page(movies)

if __name__ == '__main__':
	render()