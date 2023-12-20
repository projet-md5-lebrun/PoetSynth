import streamlit as st
import requests

st.title("Crée ton poème")
api = st.text_input('Quel est ton API token ?')
theme = st.text_input('Quel est le thème de ton poème ?')
style = st.radio("Choisis ton style", ("Classique", "Moderne"))
syl = st.radio("Choisis le nombre de syllabes", ('alexandrin', 'octosyllabe', 'décasyllabe'))

# prompt avec le thème, le style et le nombre de syllabes choisis avec des if
prompt = "Thème : " + theme + "\nStyle : " + style + "\nNombre de syllabes : " + syl + "\n\n"

if st.button("Générer"):
    API_URL = "https://api-inference.huggingface.co/models/openchat/openchat_3.5"
    headers = {"Authorization": f"Bearer {api}"}  # Utiliser f-string pour inclure la valeur de 'api'

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": f"{prompt} Ecris un poeme en francais sur {theme} de preference en {syl}. Tu dois finir les phrases ",
    })
    st.write("Voici ton poème :")
    st.markdown(output)
