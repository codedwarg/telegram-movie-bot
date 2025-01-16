Telegram Movie Bot 🎥
Overview

This Telegram bot interacts with a SQL database to search for movies based on user-defined filters such as genre, year, rating, actor, and keywords. It also logs search queries and provides statistics on the most popular queries.
Features

    Movie Search:
        Filters by genre, year, IMDb rating, keywords, and actor names.
        Retrieves data directly from a SQL database (movies).
    Query Logging:
        Logs user search queries into a separate SQL database (queries).
        Displays the most popular search queries.
    Movie Details:
        Provides detailed information: title, year, rating, genres, runtime, and poster (if available).

Installation

    Clone the repository:

git clone https://github.com/codedwarg/telegram-movie-bot.git
cd telegram-movie-bot

Install the required dependencies:

pip install -r requirements.txt

Set up the databases:

    Create a SQL database named movies and populate it with movie details (e.g., title, genres, year, rating, runtime, etc.).
    Create another SQL database named queries to log user search queries.
    Update the database connection configurations in the bot.py file.

Run the bot:

    python bot.py

Usage

    Start the bot and interact with it using the following commands:
        /start - Begin using the bot.
        /search - Search for movies by applying filters (genre, year, actor, rating, etc.).
        /popular_queries - Display the most popular search queries.

Example Output

Here’s an example of a movie search result:

Title: The Shawshank Redemption
Year: 1994
Rating: 9.3
Genres: Drama, Crime
Runtime: 142 minutes

If a movie has a poster, it will also be displayed in the chat.
Notes

    The bot uses the MySQL database for storing movie data and logging queries. Ensure the database is properly set up before running the bot.
    Replace the placeholder in bot.py with your actual Telegram Bot Token.

## Environment Variables
To run the bot, you need to define the following environment variables:
- `DB_HOST`: Database host address (e.g., `127.0.0.1`).
- `DB_USER`: Database username.
- `DB_PASSWORD`: Database password.
- `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token.


License

This project is licensed under the MIT License.
