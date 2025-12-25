import streamlit as st

def login(user, role):
    st.session_state["user"] = user
    st.session_state["role"] = role

def logout():
    st.session_state.clear()
    
def current_user():
    return st.session_state.get("user"), st.session_state.get("role")