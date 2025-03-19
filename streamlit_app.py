import streamlit as st

# Define the tabs
tabs = st.tabs(["Home", "Testimonials", "Photo Gallery", "Event Timeline"])

# Home Tab
with tabs[0]:
    st.header("Welcome to Our Wedding")
    st.image("path_to_your_image.jpg", caption="Our Engagement Photo")
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
    st.image(["photo1.jpg", "photo2.jpg", "photo3.jpg"], width=300)

# Event Timeline Tab
with tabs[3]:
    st.header("Event Timeline")
    st.write("Join us for the following events:")
    st.write("**Ceremony**: 3:00 PM at St. Mary's Church")
    st.write("**Reception**: 6:00 PM at The Grand Ballroom")
