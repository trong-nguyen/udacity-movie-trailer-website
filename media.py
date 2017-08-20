

class Movie(object):
	"""
	Class that holds properties of a movie

	Attributes:
		trailer_youtube_url (str): url to the youtube trailer of the movie
		title (str): title of the movie
		poster_image_url (str): url of the poster image
	"""
	def __init__(self, bundle):
		super(Movie, self).__init__()

		try:
			self.title = bundle['title']
			self.poster_image_url = bundle['poster_image_url']
			self.trailer_youtube_url = bundle['trailer_youtube_url']
		except KeyError as e:
			print 'Insufficient data for movie:', e.message
			raise

		