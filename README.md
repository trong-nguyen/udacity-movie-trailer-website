# Movie Trailer Website
Script to build a website displaying trailers for popular movies

## Installation
Clone the Github repository, no dependencies other than Python 2.7+.
```shell
$ git clone https://github.com/trong-nguyen/udacity-movie-trailer-website.git
```

## Usage
Change into the repo directory and run the script
```shell
$ cd [repo_directory]
$ python entertainment_center.py
```
Wait for the script to complete and `fresh_tomatoes.html` will be created with newly downloaded movie data. It will also automatically open the html file in your default browser.  
The data is fetched from themoviedatabase.org API. Modify `movie_data.get_movies_data` to change to other APIs.  

## Todos
- Test suite
- Asynchronous loading multiple urls