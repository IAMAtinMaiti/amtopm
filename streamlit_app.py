import streamlit as st

# Custom CSS to hide the GitHub icon
hide_github_icon = """
<style>
.css-1rs6os edgvbvh3 {
    display: none;
}
</style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

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

# Event Timeline Tab
with tabs[3]:
    st.header("Event Timeline")
    st.write("Join us for the following events:")
    st.write("**Ceremony**: 3:00 PM at St. Mary's Church")
    st.write("**Reception**: 6:00 PM at The Grand Ballroom")
