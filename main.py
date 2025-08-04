#
# Project 2: main.py
# Author: Jesse Martinez
# Description: A menu-driven Movie Database App that interacts with the movielens
#              database using sqlite3. It allows the user to find information about
#              movies, add reviews, get the top rated movies, set taglines. This project
#              follows N-Tier architectur, where sql queries are handled by the objecttier
#              The loop ocntinuously runs until the user enters 'x' to terminate the program
# Functions:
# - command_one(): Gives general statistics for the database. Gives information on total number
#                  of movies and reviews in the database
# - command_two(): user enters a name of the movie and the program finds the results and 
#                  prints out the id, title, and release year of the movie
# - command_three(): Find and output the detailed information about the movie. The user enters
#                    a movie_id and it retrieves the 
# - command_four(): output the top N movies based on their rating. The user enters N and
#                   the minimum number of reviews the movie needs to have
# - command_five(): allows the user to add a new review in the database
# - command_six(): Allows a user to set a tagline for a movie.
import sqlite3
import objecttier



##################################################################
# command_one:
# Description: Gives general statistics for the database. Gives information on total number
#              of movies and reviews in the database
# Parameter: dbConn - allows for connection to the database
def command_one(dbConn):
    total_movies = objecttier.num_movies(dbConn)
    total_reviews = objecttier.num_reviews(dbConn)

    if total_movies == -1 or total_reviews == -1:
        print("error")
    else:
        print("General Statistics:")
        print(f"  Number of Movies: {total_movies:,}")
        print(f"  Number of Reviews: {total_reviews:,}")
        
##################################################################  
# command_two()
# Description: user enters a name of the movie and the program finds the results and 
#              prints out the id, title, and release year of the movie
# Parameter: dbConn - allows for connection to the database
def command_two(dbConn):
    #Get the input from the user
    movie_input= input("Enter the name of the movie to find (wildcards _ and % allowed):")
    movies = objecttier.get_movies(dbConn, movie_input)
    print()
    print(f"Number of movies found: {len(movies)}")
    if len(movies) > 100:
        print()
        print("There are too many movies to display (more than 100). Please narrow your search and try again.")
    else:
        print()
        for movie in movies:
            print(f"{movie.Movie_ID} : {movie.Title} ({movie.Release_Year})")

################################################################## 
# command_three()
# Description: Find and output the detailed information about the movie. The user enters
#              a movie_id and it retrieves the data
# Parameter: dbConn - allows for connection to the database
def command_three(dbConn):
    #prompt to enter movie id
    movie_id = input("Enter a movie ID: ")
    #get the movie details from the objecttier and retrieve the data with the users input
    movie_details = objecttier.get_movie_details(dbConn, movie_id)
    
    if movie_details is None:
        #if it is empty then there is no movie that matches in the DB.
        print()
        print("No movie matching that ID was found in the database.")
    else:
        #print all the details from the objecttier (MovieDetails object)
        print()
        print(f"{movie_details.Movie_ID} : {movie_details.Title}")
        print(f"  Release date: {movie_details.Release_Date}")
        print(f"  Runtime: {movie_details.Runtime} (minutes)")
        print(f"  Original language: {movie_details.Original_Language}")
        print(f"  Budget: ${movie_details.Budget:,} (USD)")
        print(f"  Revenue: ${movie_details.Revenue:,} (USD)")
        print(f"  Number of reviews: {movie_details.Num_Reviews}")
        print(f"  Average rating: {movie_details.Avg_Rating:.2f} (0-10)")
        print(f"  Genres: {', '.join(movie_details.Genres) + ', ' if movie_details.Genres else ''}")
        print(f"  Production companies: {', '.join(movie_details.Production_Companies) + ', ' if movie_details.Production_Companies else ''}")
        print(f"  Tagline: {movie_details.Tagline}")    
##################################################################
#
# command_four()
# Description: output the top N movies based on their rating. The user enters N and
#              the minimum number of reviews the movie needs to have
# Parameter: dbConn - allows for connection to the database
def command_four(dbConn):
    # get the inputs from the user
    # - n for the number of reviews the user wants
    # - min_reviews for the minimum number of reviews per movie
    n = int(input("Enter a value for N: "))
    # validity check
    if n <= 0:
        print("Please enter a positive value for N.")
        return
    min_reviews = int(input("Enter a value for the minimum number of reviews: "))
    #validity check
    if min_reviews <= 0:
        print("Please enter a positive value for the minimum number of reviews.")
        return

    #get the information from the object tier
    top_movies = objecttier.get_top_N_movies(dbConn, n, min_reviews)

    #check for values inside of top_movies
    if not top_movies:
        print()
        print("No movies were found that fit the criteria.")
        return
    # printing the result
    print() #new line
    for movie in top_movies:
        print(f"{movie.Movie_ID} : {movie.Title} ({movie.Release_Year}), Average rating = {movie.Avg_Rating:.2f} ({movie.Num_Reviews} reviews)")

##################################################################
#
# command_five()
# Description: allows the user to add a new review in the database
# Parameter: dbConn - allows for connection in the database
def command_five(dbConn):
    #prompt to get rating from user
    rating = int(input("Enter a value for the new rating (0-10): "))
    #check validity
    if not 0 <= rating <= 10:
        print("Invalid rating. Please enter a value between 0 and 10 (inclusive).")
        return
    # prompt to get the movie id
    movie_id = input("Enter a movie ID: ")

    changedRating = objecttier.add_review(dbConn, movie_id, rating)
    if changedRating:
        print()
        print("Rating was successfully inserted into the database.")
    else:
        print()
        print("No movie matching that ID was found in the database.")

##################################################################
#
# command_six()
# Description: Allows a user to set a tagline for a movie.
# Parameter: dbConn - allows connection to the database
def command_six(dbConn):
    #prompt for a new tagline
    tagline = input("Enter a tagline: ")
    #prompt for the movie id
    movie_id = input("Enter a movie ID: ")
    #store the results from the objecttier
    added = objecttier.set_tagline(dbConn, movie_id, tagline)
    #if added returns any value then print this message
    if added:
        print()
        print("Tagline was successfully set in the database.")
    else:
        print()
        print("No movie matching that ID was found in the database.")
##################################################################
#
# main
#
print("Project 2: Movie Database App (N-Tier)")
print("CS 341, Spring 2025")
print()
print("This application allows you to analyze various")
print("aspects of the MovieLens database.")
print()
# get input from user
dbName = input("Enter the name of the database you would like to use: ")
# connect to the database
dbConn = sqlite3.connect(dbName)
print()
print("Successfully connected to the database!")

#menu loop 
while True:
    print()
    # command menu for the app
    print("Select a menu option: ")
    print("  1. Print general statistics about the database")
    print("  2. Find movies matching a pattern for the name")
    print("  3. Find details of a movie by movie ID")
    print("  4. Top N movies by average rating, with a minimum number of reviews")
    print("  5. Add a new review for a movie")
    print("  6. Set the tagline of a movie")
    print("or x to exit the program.")
    #get the command from the user
    cmd = input("Your choice --> ")
    print()

    #command one
    if cmd == "1":
        #call command_one() to handle the command
        command_one(dbConn)
    #command two
    elif cmd == "2":
        command_two(dbConn)
    #command three
    elif cmd == "3":
        command_three(dbConn)
    #command four
    elif cmd == "4":
        command_four(dbConn)
    #command five\
    elif cmd == "5":
        command_five(dbConn)
    #command six
    elif cmd == "6":
        command_six(dbConn)
    #exit
    elif cmd == "x":
        #exit out of the loop to end the game
        break
    else:
        print("Error, unknown command, try again...")



print("Exiting program.")