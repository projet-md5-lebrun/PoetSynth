import streamlit as st
from modules.db import DatabaseManager
from modules.generator import PoemGenerator

# Instantiate DatabaseManager and PoemGenerator
db_manager = DatabaseManager(db_file="./db/poem.db", data_dir="./data/db", src_db_file="poem.db")
poem_generator = PoemGenerator(db_manager=db_manager, client=None)

# Streamlit UI setup
st.set_page_config(
    page_title="Générateur de Poèmes",
    page_icon="✨",
    layout="wide"
)

# Title
st.title("Générateur de Poèmes - Explorez l'Art de la Création Poétique")

# Form components layout using columns
theme = st.text_input("Choisissez un thème", "Nature")

col_1, col_2 = st.columns([1, 1])

# Column 1
with col_1:
    nb_syllabes = st.radio("Nombre de syllabes", [6, 8, 10, 12])

# Column 2
with col_2:
    style = st.radio("Dans le style de", ["Andrée Chedid", "Charlotte Delbo", "Arthur Rimbaud", "Louis Aragon"])

# Add a space for better separation
st.write("")

# Create a simple button to generate poems
submit = st.button("Générer le poème", key='generate_button', help="Cliquez pour générer un poème")

# Handle form submission
if submit:
    # Process the form data
    generated_poem = poem_generator.generate_poem(theme, nb_syllabes, style)
    formatted_generated_poem = generated_poem.replace(",", ",<br>")

    # Display the generated poem
    st.markdown(f'<h2>Poème généré</h2>{formatted_generated_poem}', unsafe_allow_html=True)

    # Add the poem to the database
    _, total_poems = poem_generator.db_manager.add_poem(theme, nb_syllabes, style, generated_poem)
    st.success("Poème généré avec succès!")
    st.balloons()

# Create a button to clear the database
clear_db = st.button("Vider la base de données", help="Cliquez pour supprimer tous les poèmes de la base de données")

# Handle clearing the database
if clear_db:
    poem_generator.db_manager.clear_database()
    st.warning("Base de données vidée avec succès!")

# Display the latest poems
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2>Derniers poèmes générés</h2>", unsafe_allow_html=True)

latest_poems, total_poems = poem_generator.db_manager.get_latest_poems()
st.write(latest_poems)
st.markdown(f"Nombre total de poèmes générés: {total_poems}")

# Backup the database
poem_generator.db_manager.backup_db()

# Download the database
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h2>Télécharger la base de données</h2>", unsafe_allow_html=True)
st.download_button(
    label="Télécharger la base de données",
    data=latest_poems.to_csv(index=False, sep=';').encode('utf-8'),
    file_name="poem.csv",
    key='export_data',
    help="Télécharger la base de données"
)
