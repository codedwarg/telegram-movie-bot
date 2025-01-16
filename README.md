# Telegram Movie Bot 🎥

## Overview
This Telegram bot interacts with a SQL database to search for movies based on user-defined filters such as genre, year, rating, actor, and keywords. It also logs search queries and provides statistics on the most popular queries.

## Features
- **Movie Search**:
  - Filters by genre, year, IMDb rating, keywords, and actor names.
  - Retrieves data directly from an SQL database (`movies`).
- **Query Logging**:
  - Logs user search queries in a separate SQL database (`queries`).
  - Displays the most popular search queries.
- **Movie Details**:
  - Provides detailed information: title, year, rating, genres, runtime, and poster (if available).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/codedwarg/telegram-movie-bot.git
   cd telegram-movie-bot
