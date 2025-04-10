import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data = load_data('annotations.csv')

st.title("Dashboard d'analyse des annotations")

# Filtre série avec largeur réduite
col1, _ = st.columns([1, 4])
with col1:
    series = st.selectbox("Série :", ['Toutes'] + sorted(data['serie'].unique()))

filtered_data = data if series == 'Toutes' else data[data['serie'] == series]

# Pagination avec boutons rapprochés à gauche
rows_per_page = 20
total_rows = len(filtered_data)
total_pages = (total_rows - 1) // rows_per_page + 1

if 'page' not in st.session_state:
    st.session_state.page = 1

col_prev, col_next, col_page, _ = st.columns([0.1, 0.1, 0.3, 3.5])

with col_prev:
    if st.button('⬅️') and st.session_state.page > 1:
        st.session_state.page -= 1

with col_next:
    if st.button('➡️') and st.session_state.page < total_pages:
        st.session_state.page += 1

col_page.markdown(f"<div style='text-align: left; padding-top:8px;'>Page {st.session_state.page}/{total_pages}</div>", unsafe_allow_html=True)

# Afficher la table en pleine largeur
start = (st.session_state.page - 1) * rows_per_page
end = start + rows_per_page

st.dataframe(filtered_data.iloc[start:end], use_container_width=True)