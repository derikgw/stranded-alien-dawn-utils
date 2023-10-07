import database

if __name__ == "__main__":
    database.ensure_wordnet_data()
    database.create_database()  # Only run this once to create the database
    database.store_words_in_database()  # Populate the database with words. Run once or whenever you want to add more words
    print("Done...")
