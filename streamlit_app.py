import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import pytz
from datetime import datetime
import gspread
import pickle

# Define Eastern Time Zone
est = pytz.timezone("America/New_York")
json_file_path = "amtopm-454300-177900f8acb2.json"
unpickled_data = {}

# Unpickle (deserialize) the data
with open("data.pkl", "rb") as pickle_file:
    unpickled_data = pickle.load(pickle_file)

# Write dictionary to JSON file
with open(json_file_path, "w") as json_file:
    json.dump(unpickled_data, json_file, indent=4)

gc = gspread.service_account(filename=json_file_path)
sheet_testimonial = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DTB-Wnlsv80p4hCz2z0Bl5c7VEK1-ScwkKTFm-042bU/edit?usp=sharing").get_worksheet(0)
sheet_rsvp = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DTB-Wnlsv80p4hCz2z0Bl5c7VEK1-ScwkKTFm-042bU/edit?usp=sharing").get_worksheet(1)

# Function to save a new testimonial to the file
def save_testimonial(testimonial):
    """

    :param testimonial: dict
    :return:
    """
    testimonials = sheet_testimonial.get_all_records()

    if len(testimonials) == 0:

        _df = pd.DataFrame([testimonial])
        # Convert DataFrame to a list of lists
        data_list = [_df.columns.tolist()] + _df.values.tolist()

        # Update the sheet
        sheet_testimonial.update(data_list)

    else:
        testimonials.append(testimonial)
        _df = pd.DataFrame(testimonials)

        # Convert DataFrame to a list of lists
        data_list = [_df.columns.tolist()] + _df.values.tolist()

        # Update the sheet
        sheet_testimonial.update(data_list)

    print("Google Sheet updated successfully!")

# Function to save a new testimonial to the file
def save_rsvp(rsvp):
    """

    :param rsvp:
    :return:
    """
    rsvps = sheet_rsvp.get_all_records()
    print(rsvps)

    if len(rsvps) == 0:

        _df = pd.DataFrame([rsvp])
        # Convert DataFrame to a list of lists
        data_list = [_df.columns.tolist()] + _df.values.tolist()

        # Update the sheet
        sheet_rsvp.update(data_list)

    else:
        rsvps.append(rsvp)
        _df = pd.DataFrame(rsvps)

        # Convert DataFrame to a list of lists
        data_list = [_df.columns.tolist()] + _df.values.tolist()

        # Update the sheet
        sheet_rsvp.update(data_list)

    print("Google Sheet updated successfully!")

# Apply custom CSS to hide Streamlit icons
hide_streamlit_style = """
    <style>
    
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        footer:after {
                content:'goodbye'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
        }
        [data-testid="stDecoration"] {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Define the tabs
tabs = st.tabs(["Home", "Testimonials", "Photo Gallery", "Event Timeline"])

# Home Tab
with tabs[0]:
    st.header("RSVP to #AMmeetsPM")
    st.write("---")
    st.image("amtopm.jpeg", caption="Save the Date")

    # RSVP Form
    with st.expander("RSVP", expanded=True):
        with st.form(key='rsvp_form'):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            st.text('Select the dates you can attend')
            attending_23rd = st.checkbox('23rd November')
            attending_24th = st.checkbox('24th November')
            attending_26th = st.checkbox('26th November')

            # Submit button
            submit_button = st.form_submit_button(label='Submit RSVP')

            if submit_button:
                # Process the form data (e.g., save to a database or send an email)
                # Get current UTC time and convert to EST
                current_time = datetime.now(est)
                # Format as ISO 8601 string
                iso_timestamp = current_time.isoformat()

                rsvp_record = {
                        'datetime': iso_timestamp,
                        'name': name,
                        'email': email,
                        'attending_23rd': attending_23rd,
                        'attending_24th': attending_24th,
                        'attending_26th': attending_26th
                    }
                save_rsvp(rsvp_record)
                st.write(f"Thank you for your RSVP, {name}!")
                st.write(f"Email: {email}")

# Testimonials Tab
with tabs[1]:
    st.header("Testimonials")
    st.write("---")

    testimonials = sheet_testimonial.get_all_records()
    if testimonials:
        for testimonial in reversed(testimonials):
            if testimonial.get('anonymous') == 'TRUE':
                st.write(testimonial['testimonial'])
                st.write("---")
            else:
                st.write(f"**{testimonial['name']}**")
                st.write(testimonial['testimonial'])
                st.write("---")

    # Testimonials Tab
    with st.expander("Testimonials", expanded=True):
        st.header("Share Your Testimonial")
        st.write("We'd love to hear your thoughts. Please share your testimonial (up to 1000 words):")

        # Create a form for submitting testimonials
        with st.form(key='testimonial_form'):
            name = st.text_input("Your Name")
            anonymous = st.checkbox("Post Anonymously")
            testimonial_text = st.text_area("Your Testimonial", max_chars=1000)
            submit_button = st.form_submit_button(label='Submit')

            if submit_button:

                # Get current UTC time and convert to EST
                current_time = datetime.now(est)

                # Format as ISO 8601 string
                iso_timestamp = current_time.isoformat()

                if name and testimonial_text:
                    new_testimonial = {
                        'datetime': iso_timestamp,
                        'name': name,
                        'testimonial': testimonial_text,
                        'anonymous': anonymous
                    }
                    save_testimonial(new_testimonial)
                    st.success("Thank you for your testimonial!")
                else:
                    st.error("Please provide both your name and testimonial.")

# Photo Gallery Tab
with tabs[2]:
    st.header("Photo Gallery")
    st.write("---")
    st.write("A collection of our cherished moments")
    # List of image paths
    image_paths = ["amtopm.jpeg", "amtopm.jpeg", "amtopm.jpeg", "amtopm.jpeg"]

    # Define the number of columns
    num_columns = 2

    # Create columns
    cols = st.columns(num_columns)

    # Display images in columns
    for i, image_path in enumerate(image_paths):
        with cols[i % num_columns]:
            st.image(image_path)

# Event Timeline Tab
with tabs[3]:
    st.header("Event Timeline")
    st.write("---")
    st.write("Join us for the following events")
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
