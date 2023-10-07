import sqlite3


def fetch_random_word_from_database():
    conn = sqlite3.connect('word_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1")
    word = cursor.fetchone()[0]

    conn.close()
    return word


def generate_game_seed_from_database():
    word_1 = fetch_random_word_from_database()
    word_2 = fetch_random_word_from_database()

    return f"{word_1}-{word_2}"