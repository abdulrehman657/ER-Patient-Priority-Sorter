import streamlit as st

intro = st.Page(page='intro.py',title= 'Home',default = True )
test = st.Page(page='test.py',title='Try The Model')

pg = st.navigation([intro, test], position="sidebar")

pg.run()