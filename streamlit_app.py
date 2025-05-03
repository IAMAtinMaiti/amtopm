import json
import pickle
from datetime import datetime
import gspread
import mmh3
import pandas as pd
import pytz
import streamlit as st

# Define Eastern Time Zone
est = pytz.timezone("America/New_York")
json_file_path = "amtopm-gs-secret.json"
sheet_url = "https://docs.google.com/spreadsheets/d/1DTB-Wnlsv80p4hCz2z0Bl5c7VEK1-ScwkKTFm-042bU/edit?usp=sharing"
json_data = {}

# Set the maximum limit for the counter
MAX_LIMIT = 3
MIN_LIMIT = 0

# Unpickle (deserialize) the data
with open("data.pkl", "rb") as pickle_file:
    json_data = pickle.load(pickle_file)

# Write dictionary to JSON file
with open(json_file_path, "w") as json_file:
    json.dump(json_data, json_file, indent=2)

gc = gspread.service_account(filename=json_file_path)
sheet_rsvp = gc.open_by_url(sheet_url).get_worksheet(0)


# Function to save a new RSVP to the file
def save_rsvp(rsvp):
    """
    Save a new RSVP to the Google Sheet.

    :param rsvp: Dictionary containing RSVP details.
    :return: None
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
        .timeline {
            position: right;
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
            position: center;
            padding: 10px 40px;
            position: relative;
            background-color: inherit;
            width: 50%;
            margin: 10px 0;
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


def authenticate(password):
    # Define valid credentials
    return mmh3.hash(password) == 1778862707


def login_page():
    st.title("Celebrating #AMmeetsPM")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    password = st.text_input(
        "Enter the key, then click Login.", placeholder="Enter the key"
    )

    if st.button("Login"):
        if authenticate(password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid key")

    st.image("amtopm.jpeg", caption="#AMmeetsPM")


if __name__ == "__main__":

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page()
    else:
        # Define the tabs
        tabs = st.tabs(["RSVP", "Event Timeline", "Photo Gallery"])

        # Home Tab
        with tabs[0]:
            st.header("We are delighted to invite you to our wedding!")
            # RSVP Form
            with st.expander("**RSVP**", expanded=True):
                with st.form(key="rsvp_form"):
                    name = st.text_input("Full Name", placeholder="e.g., John Doe")
                    email = st.text_input(
                        "Email Address", placeholder="e.g., john.doe@gmail.com"
                    )
                    st.write("Select the dates you can attend:")
                    attending_23rd = st.checkbox("23rd November - Kolkata")
                    attending_24th = st.checkbox("24th November - Kolkata")
                    attending_26th = st.checkbox("26th November - Mumbai")
                    counter = int(
                        st.number_input(
                            "Additional guest count",
                            min_value=0,
                            max_value=3,
                            step=1,
                            key="counter",
                        )
                    )
                    song = st.text_input(
                        "Your favorite wedding jam",
                        placeholder="e.g., Mahi Ve by Shankar Ehsaan Loy",
                    )

                    # Submit button
                    submit_button = st.form_submit_button(label="**Submit RSVP**")

                    if submit_button:

                        if (
                            name
                            and email
                            and (attending_23rd or attending_24th or attending_26th)
                        ):
                            # Process the form data (e.g., save to a database or send an email)
                            # Get current UTC time and convert to EST
                            current_time = datetime.now(est).isoformat(
                                timespec="milliseconds"
                            )

                            rsvp_record = {
                                "datetime": current_time,
                                "name": name,
                                "email": email,
                                "attending_23rd": attending_23rd,
                                "attending_24th": attending_24th,
                                "attending_26th": attending_26th,
                                "guests": counter,
                                "song": song,
                            }
                            save_rsvp(rsvp_record)
                            st.write(f"Thank you for your RSVP, {name}!")
                            st.write(f"Email: {email}")

                        else:
                            st.error(
                                "Please provide your name, email, and select at least one date."
                            )

            st.video(
                "invite.MP4", format="video/mp4", autoplay=True, muted=False, loop=True
            )

        # Event Timeline Tab
        with tabs[1]:
            st.header("Event Timeline")
            st.write("---")

            # Timeline content
            timeline_data = [
                {
                    "date": "23rd November 2025: 10:00 AM IST",
                    "title": "Haldi - ঘাই হলুদ",
                    "description": "A splash of sunshine",
                    "attire": "Theme: Bright Shades",
                    "location": "Venue: New Town, Kolkata",
                },
                {
                    "date": "23rd November 2025: 07:00 PM IST",
                    "title": "Cocktail - ককটেল",
                    "description": "Raising a toast to the beginning of forever",
                    "attire": "Theme: Glitz & Glam",
                    "location": "Venue: Pride Plaza Hotel, Kolkata",
                },
                {
                    "date": "24th November 2025: 07:00 PM IST",
                    "title": "Bengali Wedding - বাঙালি হিন্দু বিবাহ",
                    "description": "Traditional bengali wedding",
                    "attire": "Theme: Traditional",
                    "location": "Venue: Pride Plaza Hotel, Kolkata",
                },
                {
                    "date": "26th November 2025: 07:00 PM IST",
                    "title": "Bou Bhat - বউ ভাত",
                    "description": "A post-wedding ritual hosted by the groom's family",
                    "attire": "Theme: Fine Dine",
                    "location": "Venue: Courtyard Navi Mumbai",
                },
            ]

            # Build the timeline
            st.markdown('<div class="timeline">', unsafe_allow_html=True)

            for i, event in enumerate(timeline_data):
                st.markdown(
                    f"""
                <div>
                    <div class="date">{event['date']}</div>
                    <div class="content">
                        <h3>{event['title']}</h3>
                        <p>{event['description']}</p>
                        <p>{event['attire']}</p>
                        <p>{event['location']}</p>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

        # Photo Gallery Tab
        with tabs[2]:
            st.header("Photo Gallery")
            st.write("---")
            st.write("Welcome to Our Love Story!")
            # List of image paths
            image_paths = ["img1.jpg", "img2.jpg"]

            # Define the number of columns
            num_columns = 2

            # Create columns
            cols = st.columns(num_columns)

            # Display images in columns
            for i, image_path in enumerate(image_paths):
                with cols[i % num_columns]:
                    st.image(image_path)

            st.write("---")
            st.write("Check back often -- more photos to come!")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
