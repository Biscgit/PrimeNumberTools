import streamlit as st

st.set_page_config(
    page_title="Faktorisierungen",
    page_icon="🔀",
)

st.title("Willkommen zu unserer Lernseite!")

st.markdown(
    "Auf der linken Seite findet ihr verschiedene Methoden welche ihr auswählen und testen könnt."
)

st.header("Was sind Primzahlen?")

st.container(height=100, border=False)
st.markdown(
    "Erstellt von Alexander Dieterich, Thomas Schauer-Köckeis und David Horvát im Rahmen der Kryptologie Vorlesung im "
    "4. Semester"
)

st.sidebar.success("Wähle eine Methode von oben aus!")
