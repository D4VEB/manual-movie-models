import psycopg2
from psycopg2.extras import DictCursor

class Movie:

    def __init__(self, movieid, title, genres):
        self.movieid = movieid
        self.title = title
        self.genres = genres

    @staticmethod
    def create_movie_from_dict(movie_dict):
        return Movie(movie_dict['movieid'], movie_dict['title'],
                    movie_dict['genres'])
        # leaving out mpaa_rating

    '''
    Create a staticmethod that will take an
    id and return one movie object with that id
    '''
    @staticmethod
    def get_by_id(cursor, id):
        cursor.execute("SELECT * FROM movies WHERE movieid = %s;", (id,))
        movie_dict = cursor.fetchone()
        return Movie.create_movie_from_dict(movie_dict)

    '''
    Create a staticmethod that takes a string
    and returns a list of movie objects that have
    that string in the title
    '''
    @staticmethod
    def get_by_string(cursor, string_in_title):
        string_to_search = "%{}".format(string_in_title)
        cursor.execute("SELECT * FROM movies WHERE lower(title) LIKE %s;", (string_to_search,))

        movies = []

        for movieid in cursor.fetchall():
            movies.append(Movie.create_movie_from_dict(movieid))
        return movies

    '''
    Create a staticmethod that takes a year and
    returns a list of movie objects that are made
    in that year
    '''

    def save(self, cursor):
        if not self.movieid:
            cursor.execute("INSERT INTO movies(title, genres) Values (%s, %s)",
                           (self.title, self.genres))
        else:
            cursor.execute("UPDATE movies SET title =%s, genres = %s WHERE movieid = %s;",
                            (self.title, self.genres, self.movieid))

    def __str__(self):
        return self.title


class Rating:

    def __init__(self, userid, movieid, rating, id):
        self.userid = userid
        self.movieid = movieid
        self.rating = rating
        self.id = id

    '''
    Create a staticmethod that takes a movie id and a
    minimum rating count and returns the average rating
    for the movie filtering based on on the minimum rating count
    '''
    @staticmethod
    def get_average_rating(cursor, movieid, review_count):
        cursor.execute("SELECT AVG(r.rating), COUNT(r.rating) FROM ratings r WHERE r.movieid = %s", (movieid,))

        # average, count = list(cursor.fetchone())
        average, count = cursor.fetchone()
        if count > review_count:
            return average
        else:
            return None


class Tag:
    def __init__(self, userid, movieid, tag, timestamp, id):
        self.userid = userid
        self.movieid = movieid
        self.tag = tag
        # self.timestamp = timestamp
        self.id = id

    '''
    Create a staticmethod that takes a movie id and
    returns a list of tags
    '''
    def movie_tags(cursor, movieid):
        cursor.execute("SELECT t.tag FROM tags t WHERE movieid = %s;", (movieid,))
        tags = cursor.fetchall()
        return [tag[0] for tag in tags]

if __name__ == '__main__':
    conn = psycopg2.connect(host="localhost", database="movies")
    cursor = conn.cursor(cursor_factory=DictCursor)

    conn.commit()

    # this is to test the get_by_id method
    # testing_id_search = Movie.get_by_id(cursor, 100)
    # print(testing_id_search)

    # this is to test the get_by_string method
    # string_search = (Movie.get_by_string(cursor, '%dog%'))
    # print(string_search)

    # to test the get_average_rating function
    # search_by_average = (Rating.get_average_rating(cursor, 1, 10))
    # print(search_by_average)

    # to test the get_average_rating function
    # get_tags = Tag.movie_tags(cursor, 500)
    # print(get_tags)