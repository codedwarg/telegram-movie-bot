import telebot
import mysql.connector
from tabulate import tabulate

# Telegram bot token
bot = telebot.TeleBot("Telegram Bot Token")

dbconfig_movies = {
    'host': 'DB_HOST',
    'user': 'DB_USER',
    'password': 'DB_PASSWORD',
    'database': 'movies'
}

dbconfig_logs = {
    'host': 'DB_HOST',
    'user': 'DB_USER',
    'password': 'DB_PASSWORD',
    'database': 'queries'
}


# Database connection and query execution
def execute_query(queries):
    movies_connection = mysql.connector.connect(**dbconfig_movies)
    movies_cursor = movies_connection.cursor()
    try:
        movies_cursor.execute(queries)
        result = movies_cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {str(e)}")
    finally:
        movies_cursor.close()
        movies_connection.close()


# Function to save logs to the database
def log_search_query(log):
    log_s_connection = mysql.connector.connect(**dbconfig_logs)
    log_s_cursor = log_s_connection.cursor()
    try:
        log_s_cursor.execute("INSERT INTO queries (log_s) VALUES (%s)", (log,))
        log_s_connection.commit()
    except Exception as e:
        print(f"Error logging: {str(e)}")
    finally:
        log_s_cursor.close()
        log_s_connection.close()


# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use the /search command to start searching for movies.")


# Function to search for movies through the bot
@bot.message_handler(commands=['search'])
def search_movies(message):
    msg = bot.reply_to(message, "Enter the year (or type * to skip):")
    bot.register_next_step_handler(msg, process_year)


def process_year(message):
    year = message.text if message.text.strip() != "" else "*"
    msg = bot.reply_to(message, "Enter the actor's name (or type * to skip):")
    bot.register_next_step_handler(msg, process_actor, year)


def process_actor(message, year):
    actor = message.text if message.text.strip() != "" else "*"
    msg = bot.reply_to(message, "Enter the desired rating from a minimum of *1* (or type * to skip):")
    bot.register_next_step_handler(msg, process_rating, year, actor)


def process_rating(message, year, actor):
    rating = message.text if message.text.strip() != "" else "*"
    msg = bot.reply_to(message, "Enter a keyword (or type * to skip):")
    bot.register_next_step_handler(msg, process_keyword, year, actor, rating)


def process_keyword(message, year, actor, rating):
    keyword = message.text if message.text.strip() != "" else "*"
    msg = bot.reply_to(message, "Enter the genre (or type * to skip):")
    bot.register_next_step_handler(msg, process_genres, year, actor, rating, keyword)


def process_genres(message, year, actor, rating, keyword):
    genres = message.text if message.text.strip() != "" else "*"
    msg = bot.reply_to(message, "How many movies should be displayed? Enter a number:")
    bot.register_next_step_handler(msg, process_limit, year, actor, rating, keyword, genres)


def process_limit(message, year, actor, rating, keyword, genres):
    try:
        limit = int(message.text)  # Number of movies to display
        conditions = []

        # Conditions where "*" means to ignore this filter
        if genres != "*":
            conditions.append(f"genres LIKE '%{genres}%'")
        if year != "*":
            conditions.append(f"year LIKE '%{year}%'")
        if actor != "*":
            conditions.append(f"cast LIKE '%{actor}%'")
        if rating != "*":
            try:
                rating = float(rating)
                conditions.append(f"`imdb.rating` >= {rating}")
            except ValueError:
                bot.reply_to(message, "Rating must be a number.")
                return
        if keyword != "*":
            conditions.append(f"(title LIKE '%{keyword}%' OR plot LIKE '%{keyword}%')")

        query = f"SELECT title, year, `imdb.rating`, genres, runtime, poster FROM movies"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += f" LIMIT {limit}"

        log = f"genres: {genres}, Year: {year}, Actor: {actor}, Rating: {rating}, Keyword: {keyword}, Limit: {limit}"
        result = execute_query(query)
        log_search_query(log)

        if result:
            for movie in result:
                title, year, imdb_rating, genres, runtime, poster = movie
                response = f"Title: {title}\nYear: {year}\nRating: {imdb_rating}\nGenres: {genres}\nRuntime: {runtime} minutes"
                bot.send_message(message.chat.id, response)
                if poster:
                    bot.send_photo(message.chat.id, poster)
                else:
                    bot.send_message(message.chat.id, "Poster not available.")
        else:
            bot.reply_to(message, "No results found!")

        # Ask about displaying popular queries after showing movies
        msg = bot.reply_to(message, "Do you want to see statistics of popular queries? (Type y/n):")
        bot.register_next_step_handler(msg, process_popular_queries)

    except ValueError:
        bot.reply_to(message, "Please enter a valid number.")


# Handling the response to the popular queries question
def process_popular_queries(message):
    answer = message.text.lower()
    if answer == "y":
        get_popular_queries(message)  # Call the function for popular queries
    else:
        show_commands(message)  # Display available commands


# Function to get popular queries
def get_popular_queries(message):
    log_s_connection = mysql.connector.connect(**dbconfig_logs)
    log_s_cursor = log_s_connection.cursor()
    try:
        sql = "SELECT log_s, COUNT(*) as count FROM queries GROUP BY log_s ORDER BY count DESC LIMIT 5"
        log_s_cursor.execute(sql)
        result = log_s_cursor.fetchall()
        if result:
            response = "Popular queries:\n"
            for row in result:
                query, count = row
                response += f"{query}: {count} times\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.reply_to(message, "No popular queries found.")
    except Exception as e:
        bot.reply_to(message, f"Error fetching popular queries: {str(e)}")
    finally:
        log_s_cursor.close()
        log_s_connection.close()

    # Show available commands after displaying statistics
    show_commands(message)


# Function to display available commands
def show_commands(message):
    commands = "/start - Start working\n/search - Find movies\n/popular_queries - Popular queries"
    bot.send_message(message.chat.id, f"Available commands:\n{commands}")


# Start the bot
bot.polling()
