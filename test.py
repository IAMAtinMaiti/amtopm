import streamlit as st

# Set the maximum limit for the counter
MAX_LIMIT = 3
MIN_LIMIT = 0

# Initialize counter in session state if not already present
if 'counter' not in st.session_state:
    st.session_state.counter = 0

def increment_counter():
    if st.session_state.counter < MAX_LIMIT:
        st.session_state.counter += 1

def decrement_counter():
    if st.session_state.counter > MIN_LIMIT:
        st.session_state.counter -= 1

st.title("Counter with Max Limit")
st.write(f"Current Count: {st.session_state.counter}")

col1, col2 = st.columns(2)

# Disable buttons if limits are reached
with col1:
    st.button("➖", on_click=decrement_counter, disabled=st.session_state.counter <= MIN_LIMIT)
with col2:
    st.button("➕", on_click=increment_counter, disabled=st.session_state.counter >= MAX_LIMIT)
