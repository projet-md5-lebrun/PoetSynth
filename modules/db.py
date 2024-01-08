import sqlite3
import pandas as pd
import shutil
import os
 
class DatabaseManager:
    def __init__(self, db_file, data_dir, src_db_file):
        self.DB_FILE = db_file
        self.DATA_DIR = data_dir
        self.SRC_DB_FILE = os.path.join(self.DATA_DIR, "poem.db")
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.DB_FILE), exist_ok=True)
        self._initialize_database()

    def _initialize_database(self):
        try:
            shutil.copyfile(self.SRC_DB_FILE, self.DB_FILE)
        except FileNotFoundError as e:
            st.warning(f"The source file {self.SRC_DB_FILE} does not exist: {e}")
        except Exception as e:
            st.warning(f"An error occurred while copying the database file: {e}")

        db = sqlite3.connect(self.DB_FILE)
        try:
            db.execute("SELECT * FROM poem").fetchall()
        except sqlite3.OperationalError:
            try:
                db.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS poem (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        theme TEXT,
                        nb_syllable INTEGER,
                        style TEXT,
                        poem TEXT
                    )
                    '''
                )
                db.commit()
            except Exception as e:
                st.warning(f"An error occurred while creating the table: {e}")
            finally:
                db.close()

    def backup_db(self):
        shutil.copyfile(self.DB_FILE, self.SRC_DB_FILE)
        db = sqlite3.connect(self.DB_FILE)
        poem = db.execute("SELECT * FROM poem").fetchall()
        pd.DataFrame(poem).to_csv(os.path.join(self.DATA_DIR, "poem.csv"), index=False)
        print("Updating the database")
        db.close()

    def get_latest_poems(self):
        db = sqlite3.connect(self.DB_FILE)
        cursor = db.cursor()
        cursor.execute("SELECT id, created_at, theme, nb_syllable, style, poem FROM poem ORDER BY id DESC limit 10")
        poem = cursor.fetchall()
        total_poem = cursor.execute("SELECT COUNT(id) FROM poem").fetchone()[0]
        columns = ["id", "created_at", "theme", "nb_syllable", "style", "poem"]
        poem_df = pd.DataFrame(poem, columns=columns)
        db.close()
        return poem_df, total_poem

    def add_poem(self, theme, nb_syllable, style, poem):
        db = sqlite3.connect(self.DB_FILE)
        cursor = db.cursor()
        cursor.execute("INSERT INTO poem(theme, nb_syllable, style, poem) VALUES(?,?,?,?)", (theme, nb_syllable, style, poem))
        db.commit()
        poem_df, total_poem = self.get_latest_poems()
        db.close()
        return poem_df, total_poem

    def load_data(self):
        db = sqlite3.connect(self.DB_FILE)
        poem_df, total_poem = self.get_latest_poems()
        db.close()
        return poem_df, total_poem