import streamlit as st
from streamlit_timeline import st_timeline
import json
import os

# Apply custom CSS to hide Streamlit icons
hide_streamlit_style = """
    <style>
    
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        @font-face {
            font-family: 'Savoye LET';
            src: url('/font/Savoye LET Plain1.0.ttf') format('truetype');
            font-weight: normal;
            font-style: normal;
        }
         
        /* Container for the tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            font-family: 'Savoye LET', sans-serif;
        }
    
        /* Individual tab style */
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #F0F2F6;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: #4f4f4f;
            font-family: 'Savoye LET', sans-serif;
        }
    
        /* Active tab style */
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            color: #000000;
            font-family: 'Savoye LET', sans-serif;
        }
        
        body {
            font-family: 'Savoye LET', sans-serif;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Event data

# Define the tabs
tabs = st.tabs(["Home", "Testimonials", "Photo Gallery", "Event Timeline"])

# Home Tab
with tabs[0]:
    st.header("Welcome to Our Wedding")
    st.image("amtopm.jpeg", caption="Our Engagement Photo")
    st.write("We are delighted to invite you to our special day!")

    # RSVP Form
    with st.form(key='rsvp_form'):
        st.subheader("RSVP Form")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        attending = st.radio("Will you be attending?", ("Yes", "No"))
        guests = st.number_input("Number of Guests", min_value=0, max_value=10, value=0)
        dietary_requirements = st.text_area("Dietary Requirements (if any)")

        # Submit button
        submit_button = st.form_submit_button(label='Submit RSVP')

        if submit_button:
            # Process the form data (e.g., save to a database or send an email)
            st.write(f"Thank you for your RSVP, {name}!")
            st.write(f"Email: {email}")
            st.write(f"Attending: {attending}")
            st.write(f"Number of Guests: {guests}")
            st.write(f"Dietary Requirements: {dietary_requirements}")

# File to store testimonials
TESTIMONIALS_FILE = 'testimonials.json'

# Function to load testimonials from the file
def load_testimonials():
    if os.path.exists(TESTIMONIALS_FILE):
        with open(TESTIMONIALS_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

# Function to save a new testimonial to the file
def save_testimonial(testimonial):
    testimonials = load_testimonials()
    testimonials.append(testimonial)
    with open(TESTIMONIALS_FILE, 'w') as file:
        json.dump(testimonials, file, indent=4)

# Testimonials Tab
with tabs[1]:
    st.header("Testimonials")
    st.write("Here's what our friends and family say about us:")
    st.write("- *'A match made in heaven!'* – Jane Doe")
    st.write("- *'Two beautiful souls coming together.'* – John Smith")

    # Testimonials Tab
    with st.expander("Testimonials", expanded=True):
        st.header("Share Your Testimonial")
        st.write("We'd love to hear your thoughts. Please share your testimonial (up to 1000 words):")

        # Create a form for submitting testimonials
        with st.form(key='testimonial_form'):
            name = st.text_input("Your Name")
            testimonial_text = st.text_area("Your Testimonial", max_chars=1000)
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:
                if name and testimonial_text:
                    new_testimonial = {
                        'name': name,
                        'testimonial': testimonial_text
                    }
                    save_testimonial(new_testimonial)
                    st.success("Thank you for your testimonial!")
                else:
                    st.error("Please provide both your name and testimonial.")

        # Display existing testimonials
        st.subheader("What Others Are Saying")
        testimonials = load_testimonials()
        if testimonials:
            for testimonial in reversed(testimonials):
                st.write(f"**{testimonial['name']}**")
                st.write(testimonial['testimonial'])
                st.write("---")
        else:
            st.write("No testimonials yet. Be the first to share!")

# Photo Gallery Tab
with tabs[2]:
    st.header("Photo Gallery")
    st.write("A collection of our cherished moments:")
    # List of image paths
    image_paths = ["amtopm.jpeg", "amtopm.jpeg", "amtopm.jpeg", "amtopm.jpeg"]

    # Define the number of columns
    num_columns = 2

    # Create columns
    cols = st.columns(num_columns)

    # Display images in columns
    for i, image_path in enumerate(image_paths):
        with cols[i % num_columns]:
            st.image(image_path, use_container_width=True)

# Event Timeline Tab
with tabs[3]:
    st.header("Event Timeline")
    st.write("Join us for the following events:")
    st.set_page_config(page_title="Event Timeline", layout="wide")

    # Title of the app
    st.title("Interactive Timeline with Hover Popups")

    # Timeline data
    timeline_data = [
        {'content': 'Event 1: Project Initiation', 'start': '2025-01-01'},
        {'content': 'Event 2: Development Phase', 'start': '2025-02-01'},
        {'content': 'Event 3: Testing and QA', 'start': '2025-03-01'},
        {'content': 'Event 4: Deployment', 'start': '2025-04-01'},
        {'content': 'Event 5: Post-Launch Review', 'start': '2025-05-01'},
    ]

    # Display the timeline
    st_timeline(timeline_data, height=600)