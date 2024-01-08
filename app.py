import streamlit as st
#from huggingface_hub import InferenceClient
from modules.db import DatabaseManager
import modules.geneator import ...
"""class PoemGenerator:
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
"""
# Instantiate DatabaseManager and PoemGenerator
db_manager = DatabaseManager(db_file="./db/poem.db", data_dir="./data/db", src_db_file="poem.db")
client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")
poem_generator = PoemGenerator(db_manager=db_manager, client=client)


# Define the Streamlit app
# New front design for the app 

    def run_streamlit_app(self):
        # Streamlit UI setup
        st.title("Poem Generator")

        # Create form components for theme, syllables, and style
        theme = st.text_input("Choisir un théme", "Nature, amour, temps, ...")
        nb_syllabes = st.radio("Number of syllables", [6, 8, 10, 12])
        style = st.radio("In the style of", ["Andrée Chedid", "Charlotte Delbo", "Arthur Rimbaud", "Louis Aragon"])
        submit = st.button("Création du poème")

        # Handle form submission
        if submit:
            # Process the form data
            generated_poem = self.generate_poem(theme, nb_syllabes, style)
            formatted_generated_poem = generated_poem.replace(",", ",<br>")

            # Display the generated poem
            st.markdown(f"## Generated Poem\n{formatted_generated_poem}", unsafe_allow_html=True)

            # Add the poem to the database
            self.db_manager.add_poem(theme, nb_syllabes, style, generated_poem)
            st.success("Poem generated and saved successfully!")

        # Display a summary of the latest poems and provide a download button for the CSV file
        data, count = self.db_manager.load_data()
        st.dataframe(data)
        st.download_button("Download Data as CSV", data.to_csv(), "poem.csv", "text/csv")


# Run the Streamlit app
poem_generator.run_streamlit_app()
