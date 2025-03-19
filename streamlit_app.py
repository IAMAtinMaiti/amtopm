import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import os
from streamlit_option_menu import option_menu

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
        
        body {
            font-family: 'Savoye LET', sans-serif;
        }
         
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
        }
    
        /* Active tab style */
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            color: #000000;
        }
        
        /* Move the sidebar to the right */
        .css-1d391kg {flex-direction: row-reverse;}

        /* Set the sidebar background color to orange */
        .css-1d391kg .css-17eq0hr {
            background-color: orange;
        }
        .stApp {
            background-color: #D3D3D3;  /* Light gray color */
        }
        
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# st.set_page_config(
#     page_title="Wedding Event",
#     layout="wide",
#     initial_sidebar_state="expanded"  # Sidebar is always expanded
# )

# Sidebar navigation
#selection = st.sidebar.selectbox("Navigation", ["Home", "Testimonials", "Gallery", "Event Timeline"])
selection = option_menu("Navigation", ["Home", "Testimonials", "Gallery", "Event Timeline"])


# Display content based on selection
if selection == "Home":
    st.title("Home")
    st.write("Welcome to our wedding event website!")
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


elif selection == "Testimonials":
    st.title("Testimonials")
    st.write("Read what our guests have to say.")
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

elif selection == "Gallery":
    st.title("Gallery")
    st.write("View photos from our special day.")
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

elif selection == "Event Timeline":
    st.title("Event Timeline")
    st.write("See the schedule of events.")
    st.header("Event Timeline")
    st.write("Join us for the following events:")
    fig = go.Figure()

    data = {
        "Title": ["Event 1", "Event 2", "Event 3"],
        "Description": ["Description of Event 1", "Description of Event 2", "Description of Event 3"],
        "Date": ["2025-01-01", "2025-02-01", "2025-03-01"]
    }
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])

    for i, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Date"], row["Date"]],
            y=[i, i],
            mode="lines+markers+text",
            marker=dict(size=12, color="blue"),
            line=dict(width=2, color="blue"),
            text=row["Title"],
            textposition="top center",
            hoverinfo="text+name"
        ))

    fig.update_layout(
        title="Interactive Timeline",
        xaxis_title="Date",
        yaxis=dict(
            tickvals=list(range(len(df))),
            ticktext=df["Title"].tolist()
        ),
        showlegend=False,
        hovermode="closest"
    )

    st.plotly_chart(fig)