import os
import random
import sqlite3
import nltk
from nltk.corpus import wordnet


def ensure_wordnet_data():
    """
    Ensure that WordNet data is downloaded.
    """
    try:
        wordnet.words()  # Try accessing WordNet data
    except LookupError:
        nltk.download('wordnet')  # If not found, download it


def drop_words_table():
    conn = sqlite3.connect('word_database.db')
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS words''')  # Drop the table if it exists

    conn.commit()
    conn.close()


def create_database():
    print("Creating database...")

    nltk.download('wordnet')

    db_file = 'word_database.db'

    # If database file exists, drop the words table
    if os.path.exists(db_file):
        drop_words_table()

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS words (word TEXT)''')

    conn.commit()
    conn.close()


def fetch_word_from_wordnet():
    while True:  # Keep looking until a suitable word is found
        synsets = list(wordnet.all_synsets())  # Get all synsets
        word = random.choice(synsets).lemmas()[0].name()  # Randomly select a synset and get its first lemma (word)
        word = word.replace("_", " ")  # Convert underscores (if any) to spaces

        if '-' not in word and ' ' not in word:
            return word  # Only return words without hyphens or spaces


def store_words_in_database(num_words=200):
    conn = sqlite3.connect('word_database.db')
    cursor = conn.cursor()

    for _ in range(num_words):
        word = fetch_word_from_wordnet()
        print(f"Storing word: {word}")
        cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))

    conn.commit()
    conn.close()


def get_word_count():
    conn = sqlite3.connect('word_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(word) FROM words")
    count = cursor.fetchone()[0]
    conn.close()
    return count
