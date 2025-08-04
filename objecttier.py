#
# objecttier.py
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author: Ellen Kidane and Prof. Joe Hummel
# Current author: Jesse Martinez
#
# Classes: 
# - Movie : contains movie movie details 
# - MovieRating: contains rating information on the movie
# - MovieDetails: Contains detailed information about the movie, including genres and production companies
#
# Functions:
# - num_movies(dbConn): Returns the number of movies in the database.
# - num_reviews(dbConn): Returns the number of reviews in the database.
# - get_movies(dbConn, pattern): Retrieves movies matching a title pattern.
# - get_movie_details(dbConn, movie_id): Retrieves detailed information for a movie.
# - get_top_N_movies(dbConn, N, min_num_reviews): Retrieves the top N movies by rating.
# - add_review(dbConn, movie_id, rating): Adds a user rating for a given movie.
# - set_tagline(dbConn, movie_id, tagline): Updates or inserts a movie's tagline.
#
# ** !! This file relies on datatier.py to interact with the database
import datatier

##################################################################
#
# Movie class:
# - Contains basic movie details:
#    + Constructor(...)
#    + Properties:
#      > Movie_ID: int
#      > Title: string
#      > Release_Year: string
#
class Movie:
    # constructor to initialize all variables in the class
    def __init__(self, Movie_ID, Title, Release_Year):
        self._Movie_ID = Movie_ID
        self._Title = Title
        self._Release_Year = Release_Year

    #read only properties for functions

    # Movie_ID : int
    @property
    def Movie_ID(self):
        return self._Movie_ID

    # Title : string
    @property
    def Title(self):
        return self._Title

    # Release_Year : string
    @property
    def Release_Year(self):
        return self._Release_Year

##################################################################
#
# MovieRating class:
#  - Contains rating details on movies in the database:
#     + Constructor(...)
#     + Properties:
#       > Movie_ID: int
#       > Title: string
#       > Release_Year: string
#       > Num_Reviews: int
#       > Avg_Rating: float
#
class MovieRating:
    # Constructor
    def __init__(self, Movie_ID, Title, Release_Year, Num_Reviews, Avg_Rating):
        self._Movie_ID = Movie_ID
        self._Title = Title
        self._Release_Year = Release_Year
        self._Num_Reviews = Num_Reviews
        self._Avg_Rating = Avg_Rating

    #read only property functions

    # Movie_ID : int
    @property
    def Movie_ID(self):
        return self._Movie_ID

    # Title : string
    @property
    def Title(self):
        return self._Title

    # Release_Year : string
    @property
    def Release_Year(self):
        return self._Release_Year

    # Num_Reviews : int
    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    # Avg_Rating : float
    @property
    def Avg_Rating(self):
        return self._Avg_Rating

##################################################################
#
# MovieDetails class:
# - Contains details about the movie:
#   + Constructor(...)
#   + Properties:
#     > Movie_ID: int
#     > Title: string
#     > Release_Date: string
#     > Runtime: int (minutes)
#     > Original_Language: string
#     > Budget: int (USD)
#     > Revenue: int (USD)
#     > Num_Reviews: int
#     > Avg_Rating: float
#     > Tagline: string
#     > Genre : list
#     > Production_company : list
class MovieDetails:
    # Constructor
    def __init__(self, Movie_ID, Title, Release_Date, Runtime, Original_Language, Budget, Revenue, Num_Reviews, Avg_Rating, Tagline, Genres, Production_Companies):
        self._Movie_ID = Movie_ID
        self._Title = Title
        self._Release_Date = Release_Date
        self._Runtime = Runtime
        self._Original_Language = Original_Language
        self._Budget = Budget
        self._Revenue = Revenue
        self._Num_Reviews = Num_Reviews
        self._Avg_Rating = Avg_Rating
        self._Tagline = Tagline
        self._Genres = Genres
        self._Production_Companies = Production_Companies
    
    #read only property functions

    # Movie_ID : int
    @property
    def Movie_ID(self):
        return self._Movie_ID

    # Title : string
    @property
    def Title(self):
        return self._Title

    # Release_Date : string
    @property
    def Release_Date(self):
        return self._Release_Date

    # Runtime : int (minutes)
    @property
    def Runtime(self):
        return self._Runtime

    # Original_Language : string
    @property
    def Original_Language(self):
        return self._Original_Language

    # Budget : int (USD)
    @property
    def Budget(self):
        return self._Budget

    # Revenue : int (USD)
    @property
    def Revenue(self):
        return self._Revenue

    # Num_Reviews : int 
    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    # Avg_Rating : float
    @property
    def Avg_Rating(self):
        return self._Avg_Rating

    # Tagline : string
    @property
    def Tagline(self):
        return self._Tagline
    # genre : string
    @property
    def Genres(self):
        return self._Genres
    
    #production_company : string
    @property
    def Production_Companies(self):
        return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: the number of movies in the database, or
#          -1 if an error occurs
# 
def num_movies(dbConn):
    try:
        # query to count all the movies in the database
        movies= """
        SELECT 
            COUNT(*)
        FROM
            Movies
        """
        # execute the query and store the results
        row = datatier.select_one_row(dbConn, movies)
        
        if row is None:
            #if not found, then return -1
            return -1
        else:
            #if found, return the number of movies there are in the database
            return row[0]
    except:
        return -1

##################################################################
# 
# num_reviews:
#
# Returns: the number of reviews in the database, or
#          -1 if an error occurs
#
def num_reviews(dbConn):
    try:
        #query to get the total number of reviews in the database
        reviews  = """
        SELECT
            COUNT(*)
        FROM
            Ratings
        """
        # execute the query and store the results
        row = datatier.select_one_row(dbConn, reviews)
        if row is None:
            #if not found, then return -1
            return -1
        else:
            #if found, return the number of movies there are in the database
            return row[0]
    except:
        return -1

##################################################################
#
# get_movies:
#
# Finds and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all movies.
#
# Returns: list of movies in ascending order by name, or
#          an empty list, which means that the query did 
#          not retrieve any data
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_movies(dbConn, pattern):
    try:
        # query that gets the basic movie details (movie_id, title, and the year of release) of a specific movie
        # ordered by movie_id in ascending order
        movies = """
        SELECT
            Movie_ID, Title, strftime('%Y', Release_Date)
        FROM
            Movies
        WHERE
            Title LIKE ?
        ORDER BY
            Movie_ID ASC
        """
        # execute the query and store the results
        rows = datatier.select_n_rows(dbConn, movies, [pattern])
        # store the result as a Movie object if it exists, else: empty list
        result = [Movie(row[0], row[1], row[2]) for row in rows] if rows else []
        #return the Movie objects 
        return result
    except:
        return []

##################################################################
#
# get_movie_details:
#
# Finds and returns details about the given movie.
# The movie ID is passed as a parameter (originally from the user)
# and the function returns a MovieDetails object.
# If no movie was found matching that ID, the function returns
# None.
#
# Returns: a MovieDetails object if the search was successful, or
#          None if the search did not find a matching movie
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_movie_details(dbConn, movie_id):
    try:
        
        # query that retrieves the movie details (movie_id, title, release_date, runtime, original_language, budget, revenue,
        # number of reviews, average rating, and tagline) of a specific movie. Joined with 2 other tables in the database, matching their movie_id's
        # and grouped by the movie id.
        details = """
        SELECT
            m.Movie_ID, m.Title, DATE(m.Release_Date), m.Runtime, m.Original_Language,
            m.Budget, m.Revenue,
            COUNT(r.Rating) AS num_reviews, 
            IFNULL(AVG(r.Rating), 0) as avg_rating,
            mt.Tagline
        FROM
            Movies m
        LEFT JOIN Ratings r ON m.Movie_ID = r.Movie_ID
        LEFT JOIN Movie_Taglines mt ON m.Movie_ID = mt.Movie_ID
        WHERE
            m.Movie_ID = ?
        GROUP BY
            m.Movie_ID
        """ 
        
        #execute the query and store the results
        row = datatier.select_one_row(dbConn, details, [movie_id])
        
        #check to see if the data was found
        if row is None:
            return None #if not found, return none

        #handle the missing tagline
        if row[9] is not None:
            tagline = row[9]
        else:
            tagline = ""
        
        # query to get the genre of the movie the user has selected. Ordered by the genre name
        genres_sql = """
        SELECT
            g.Genre_Name
        FROM
            Genres g
        JOIN
            Movie_Genres mg ON g.Genre_ID = mg.Genre_ID
        WHERE 
            mg.Movie_ID = ?
        ORDER BY 
            g.Genre_Name ASC
        """
        #execute and store the results
        genre_results = datatier.select_n_rows(dbConn, genres_sql, [movie_id])
        
        #add to the list of genres
        genres = [genre[0] for genre in genre_results] if genre_results else []

        #get the production company of a movie the user selected and ordered by comapny name in ascending order
        companies_sql = """
        SELECT
            c.Company_Name
        FROM
            Companies c
        JOIN
            Movie_Production_Companies mpc ON c.Company_ID = mpc.Company_ID
        WHERE
            mpc.Movie_ID = ?
        ORDER BY
            c.Company_Name ASC
        """
        # execute and store the results
        companies_results = datatier.select_n_rows(dbConn, companies_sql, [movie_id])

        #add to the list of companies
        companies = [company[0] for company in companies_results] if companies_results else []

        #return the object MovieDetails
        return MovieDetails(
            row[0], row[1], row[2], row[3], row[4], 
            row[5], row[6], row[7], row[8], tagline,
            genres, companies
        )
    except:
        return None
         

##################################################################
#
# get_top_N_movies:
#
# Finds and returns the top N movies based on their average 
# rating, where each movie has at least the specified number of
# reviews.
# Example: get_top_N_movies(10, 100) will return the top 10 movies
#          with at least 100 reviews.
#
# Returns: a list of 0 or more MovieRating objects
#          note that if the list is empty, it may be because the 
#          minimum number of reviews was too high
#          (or an internal error occurred, in which case 
#          an error message is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
    try:
        # query that gets the movie_id, title, release year, number of reviews, and average rating of movies. Number of movies depend on users input
        ratings = """
        SELECT
            m.Movie_ID, m.Title, strftime('%Y', m.Release_Date),
            COUNT(r.Rating) as Num_Reviews,
            CAST(AVG(r.Rating) AS FLOAT) as Avg_Rating
        FROM
            Movies m 
        JOIN Ratings r on m.Movie_ID = r.Movie_ID
        GROUP BY 
            m.Movie_ID
        HAVING
            Num_Reviews >= ?
        ORDER BY
            Avg_Rating DESC
        LIMIT ?
        """
        # execute and store the results of the query
        rows = datatier.select_n_rows(dbConn, ratings, [min_num_reviews, N])
        #store the results in the movieRating object if it exists
        top_movies = [
            MovieRating(row[0], row[1], row[2], row[3], row[4]) for row in rows
            ] if rows else []

        return top_movies
    except:
        return []

##################################################################
#
# add_review:
#
# Inserts the given review (a rating value between 0 and 10) into
# the database for the given movie.
# It is considered an error if the movie does not exist, and 
# the review is not inserted.
#
# Returns: 1 if the review was successfully added, or
#          0 if not (e.g. if the movie does not exist, or
#                    if an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
    try:
        #find the movie that we want to add the review to based on movie_id
        find_movie = """
        SELECT
            1
        FROM
            Movies
        WHERE
            Movie_ID = ?
        """
        row = datatier.select_one_row(dbConn, find_movie, [movie_id])
        #if we cant find the movie_id, then return 0
        if row is None or row[0] == 0:
            return 0
        
        # add the review into the reviews table
        insert_review = """
        INSERT INTO
            Ratings (Movie_ID, Rating)
        VALUES
            (?, ?)
        """
        #call perform action to handle the insert method
        rows_changed = datatier.perform_action(dbConn, insert_review, [movie_id, rating])

        return 1 if rows_changed > 0 else 0 #return 1 if success, 0 for failure
    except:
        return 0 #fail


##################################################################
#
# set_tagline:
#
# Sets the tagline, i.e. summary, for the given movie.
# If the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline.
# It is considered an error if the movie does not exist, and 
# the tagline is not set.
#
# Returns: 1 if the tagline was successfully set, or
#          0 if not (e.g. if the movie does not exist, or
#                    if an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    try:
        #query to check if the movie exists in the database based on the movie_id
        exists = """
        SELECT 
            1
        FROM 
            Movies
        WHERE
            Movie_ID = ?
        """
        #execute and store the result of the movie existing 
        result = datatier.select_one_row(dbConn, exists, [movie_id])
        
        #if the movie does not exist or exists as () then return 0
        if result is None or result == ():
            return 0 # movie does not exist
    
        #check if a tagline exists for the movie
        tagline_sql = """
        SELECT 
            COUNT(*)
        FROM 
            Movie_Taglines
        WHERE
            Movie_ID = ?
        """
        #execute the query and store its results
        tagline_result = datatier.select_one_row(dbConn, tagline_sql, [movie_id])
        
        #if there is no result, then return 0
        if tagline_result is None:
            return 0

        #update the table and set the tagline
        update_sql = """
            UPDATE Movie_Taglines 
            SET Tagline = ? 
            WHERE Movie_ID = ?
        """
        #insert a new one
        insert_sql = """
        INSERT INTO Movie_Taglines (Movie_ID, Tagline)
        VALUES (?, ?)
        """
        #Initialize to 0 
        changed = 0
        #print(f"tagline results: {tagline_result}")
        if tagline_result[0] > 0:
            #UPDATE
            #execute the query and store the results
            changed = datatier.perform_action(dbConn, update_sql, [tagline, movie_id])
        else:
            #INSERT
            #execute and store the results
            changed = datatier.perform_action(dbConn, insert_sql, [movie_id, tagline])
        
        #if any changes were made, then return 1 for success, 0 for failure
        return 1 if changed > 0 else 0
    except:
        return 0