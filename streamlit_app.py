import streamlit as st
from streamlit_timeline import st_timeline

# Event data

# Define the tabs
tabs = st.tabs(["Home", "Testimonials", "Photo Gallery", "Event Timeline"])

# Home Tab
with tabs[0]:
    st.header("Welcome to Our Wedding")
    st.image("amtopm.jpeg", caption="Our Engagement Photo")
    st.write("We are delighted to invite you to our special day!")

# Testimonials Tab
with tabs[1]:
    st.header("Testimonials")
    st.write("Here's what our friends and family say about us:")
    st.write("- *'A match made in heaven!'* – Jane Doe")
    st.write("- *'Two beautiful souls coming together.'* – John Smith")

# Photo Gallery Tab
with tabs[2]:
    st.header("Photo Gallery")
    st.write("A collection of our cherished moments:")
    st.image(["amtopm.jpeg", "amtopm.jpeg", "amtopm.jpeg"], width=300)

events = [
    {"id": 1, "content": "Ceremony", "start": "2025-06-15T15:00:00", "end": "2025-06-15T16:00:00"},
    {"id": 2, "content": "Reception", "start": "2025-06-15T18:00:00", "end": "2025-06-15T23:00:00"},
    {"id": 3, "content": "After Party", "start": "2025-06-16T00:00:00", "end": "2025-06-16T02:00:00"},
]

# Event Timeline Tab
with tabs[3]:
    st.header("Event Timeline")
    timeline = st_timeline(events, groups=[], options={}, height="400px")

