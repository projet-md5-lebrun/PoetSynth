import streamlit as st
import sqlite3
import pandas as pd
import shutil
from huggingface_hub import InferenceClient
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


class PoemGenerator:
    def __init__(self, db_manager, client):
        self.db_manager = db_manager
        self.client = client

    def format_prompt(self, theme, nb_syllabes, style, message):
        prompt = f"Create a poem in French on the theme {theme}, preferably in {nb_syllabes} syllables. In the style of the poet {style}. It should end with a dot.  <s> [INST] {message} [/INST]"
        return prompt

    def generate_poem(self, theme, syl, style, temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0):
        temperature = float(temperature)
        if temperature < 1e-2:
            temperature = 1e-2
        top_p = float(top_p)

        generate_kwargs = dict(
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            do_sample=True,
            seed=42,
        )

        formatted_prompt = self.format_prompt(theme, syl, style, message="your_message_here")
        stream = self.client.text_generation(
            formatted_prompt,
            **generate_kwargs,
            stream=True,
            details=True,
            return_full_text=False
        )

        output = ""
        for response in stream:
            output += response.token.text

        return output

    def run_streamlit_app(self):
        # Streamlit UI setup
        st.title("Générateur de Poèmes")

        # Create form components for theme, syllables, and style
        theme = st.text_input("Choisissez le thème", "Nature")
        nb_syllabes = st.radio("Nombre de syllabes", [6, 8, 10, 12])
        style = st.radio("Dans le style de", ["Andrée Chedid", "Charlotte Delbo", "Arthur Rimbaud", "Louis Aragon"])
        submit = st.button("Générer le poème")

        # Handle form submission
        if submit:
            # Process the form data
            generated_poem = self.generate_poem(theme, nb_syllabes, style)
            formatted_generated_poem = generated_poem.replace(",", ",<br>")

            # Display the generated poem
            st.markdown(f"## Poème généré\n{formatted_generated_poem}", unsafe_allow_html=True)

            # Add the poem to the database
            self.db_manager.add_poem(theme, nb_syllabes, style, generated_poem)
            st.success("Poème généré et sauvegardé avec succès!")

        # Display a summary of the latest poems and provide a download button for the CSV file
        data, count = self.db_manager.load_data()
        st.dataframe(data)
        st.download_button("Télécharger les données en CSV", data.to_csv(), "poem.csv", "text/csv")

# Instantiate DatabaseManager and PoemGenerator
db_manager = DatabaseManager(db_file="./db/poem.db", data_dir="./data/db", src_db_file="poem.db")
client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")
poem_generator = PoemGenerator(db_manager=db_manager, client=client)

# Run the Streamlit app
poem_generator.run_streamlit_app()