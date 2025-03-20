import streamlit as st
import pandas as pd
import json
import pytz
from datetime import datetime
import gspread
import pickle

# Define Eastern Time Zone
est = pytz.timezone("America/New_York")
json_file_path = "amtopm-gs-secret.json"
sheet_url= "https://docs.google.com/spreadsheets/d/1DTB-Wnlsv80p4hCz2z0Bl5c7VEK1-ScwkKTFm-042bU/edit?usp=sharing"
json_data = {}

# Unpickle (deserialize) the data
with open("data.pkl", "rb") as pickle_file:
    json_data = pickle.load(pickle_file)

# Write dictionary to JSON file
with open(json_file_path, "w") as json_file:
    json.dump(json_data, json_file, indent=2)

gc = gspread.service_account(filename=json_file_path)
sheet_testimonial = gc.open_by_url(sheet_url).get_worksheet(0)
sheet_rsvp = gc.open_by_url(sheet_url).get_worksheet(1)

# Function to save a new testimonial to the file
def save_testimonial(record):
    """

    :param record: dict
    :return:
    """
    sheet_testimonial = gc.open_by_url(sheet_url).get_worksheet(0)
    records = sheet_testimonial.get_all_records()

    if len(testimonials) == 0:

        _df = pd.DataFrame([record])
        # Convert DataFrame to a list of lists
        data_list = [_df.columns.tolist()] + _df.values.tolist()

        # Update the sheet
        sheet_testimonial.update(data_list)

    else:
        records.append(record)
        _df = pd.DataFrame(records)

        # Convert DataFrame to a list of lists
        data_list = [_df.columns.tolist()] + _df.values.tolist()

        # Update the sheet
        sheet_testimonial.update(data_list)

    print("Google Sheet updated successfully!")

# Function to save a new rsvp to the file
def save_rsvp(rsvp):
    """

    :param rsvp:
    :return:
    """
    sheet_rsvp = gc.open_by_url(sheet_url).get_worksheet(1)
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
        .timeline {
            position: relative;
            max-width: 900px;
            margin: 0 auto;
        }
        .timeline::after {
            content: '';
            position: absolute;
            width: 6px;
            background-color: #3e3e3e;
            top: 0;
            bottom: 0;
            left: 50%;
            margin-left: -3px;
        }
        .container {
            padding: 10px 40px;
            position: relative;
            background-color: inherit;
            width: 50%;
            margin: 10px 0;
        }
        .container.left {
            left: 0;
        }
        .container.right {
            left: 50%;
        }
        .date {
            position: center;
            top: 100%;
            transform: translateY(-20%);
            padding: 5px 10px;
            background-color: #333;
            color: white;
            border-radius: 4px;
            font-size: 14px;
        }
        .content {
            padding: 20px;
            border-radius: 6px;
        }
    </style>
"""
st.set_page_config(page_title="#AMmeetsPM")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Define the tabs
tabs = st.tabs(["Home", "Event Timeline", "Testimonials", "Photo Gallery"])

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
            st.write('Select the dates you can attend')
            attending_23rd = st.checkbox('23rd November')
            attending_24th = st.checkbox('24th November')
            attending_26th = st.checkbox('26th November')

            # Submit button
            submit_button = st.form_submit_button(label='Submit RSVP')

            if submit_button:
                # Process the form data (e.g., save to a database or send an email)
                # Get current UTC time and convert to EST
                current_time = datetime.now(est).isoformat(timespec='milliseconds')

                rsvp_record = {
                        'datetime': current_time,
                        'name': name,
                        'email': email,
                        'attending_23rd': attending_23rd,
                        'attending_24th': attending_24th,
                        'attending_26th': attending_26th
                    }
                save_rsvp(rsvp_record)
                st.write(f"Thank you for your RSVP, {name}!")
                st.write(f"Email: {email}")

# Event Timeline Tab
with tabs[1]:
    st.header("Event Timeline")
    st.write("---")

    # Timeline content
    timeline_data = [
        {"date": "January 2022", "title": "Project Started", "description": "Kickoff of the new project."},
        {"date": "March 2022", "title": "First Milestone", "description": "Completed the first milestone."},
        {"date": "June 2022", "title": "Phase 2", "description": "Transitioned to phase 2."},
        {"date": "September 2022", "title": "Final Review", "description": "Completed the final review."},
        {"date": "December 2022", "title": "Project Complete", "description": "Project completed successfully."}
    ]

    # Build the timeline
    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for i, event in enumerate(timeline_data):
        position = "left" if i % 2 == 0 else "right"
        st.markdown(f'''
        <div class="container {position}">
            <div class="date">{event['date']}</div>
            <div class="content">
                <h3>{event['title']}</h3>
                <p>{event['description']}</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Testimonials Tab
with tabs[2]:
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
                current_time = datetime.now(est).isoformat(timespec='milliseconds')

                if name and testimonial_text:
                    new_testimonial = {
                        'datetime': current_time,
                        'name': name,
                        'testimonial': testimonial_text,
                        'anonymous': anonymous
                    }
                    save_testimonial(new_testimonial)
                    st.success("Thank you for your testimonial!")
                else:
                    st.error("Please provide both your name and testimonial.")

# Photo Gallery Tab
with tabs[3]:
    st.header("Photo Gallery")
    st.write("---")
    st.write("A collection of our cherished moments")
    # List of image paths
    image_paths = ["img1.jpg", "img2.jpg", "img4.jpg", "img5.jpg"]

    # Define the number of columns
    num_columns = 2

    # Create columns
    cols = st.columns(num_columns)

    # Display images in columns
    for i, image_path in enumerate(image_paths):
        with cols[i % num_columns]:
            st.image(image_path)

