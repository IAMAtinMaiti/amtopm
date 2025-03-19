import streamlit as st

# Apply custom CSS to hide Streamlit icons
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Container for the tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
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
            font-family: 'Courier New', Courier, monospace;
        }
    
        /* Active tab style */
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            color: #000000;
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
