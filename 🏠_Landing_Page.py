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

st.markdown(
    "Primzahlen sind natürliche Zahlen größer als 1, die nur durch 1 und sich selbst teilbar sind. "
    "Das bedeutet, dass sie keine anderen positiven Teiler haben. "
    "Primzahlen spielen eine zentrale Rolle in der Mathematik, insbesondere in der Zahlentheorie, und haben wichtige "
    "Anwendungen in der Kryptographie und der Informatik. Sie sind unendlich viele und es gibt keinen einfachen "
    "Algorithmus, um sie alle zu finden, was ihre Untersuchung besonders spannend und herausfordernd macht."
)
st.markdown(
    "**2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...**"
)


st.container(height=100, border=False)
st.markdown(
    "Erstellt von Alexander Dieterich, Thomas Schauer-Köckeis und David Horvát im Rahmen der Kryptologie Vorlesung im "
    "4. Semester"
)

st.sidebar.success("Wähle eine Methode von oben aus!")
