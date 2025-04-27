import streamlit as st
import pandas as pd
import json
import pytz
from datetime import datetime
import gspread
import pickle
import mmh3

# Define Eastern Time Zone
est = pytz.timezone("America/New_York")
json_file_path = "amtopm-gs-secret.json"
sheet_url= "https://docs.google.com/spreadsheets/d/1DTB-Wnlsv80p4hCz2z0Bl5c7VEK1-ScwkKTFm-042bU/edit?usp=sharing"
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

    password = st.text_input("Enter the key, then click Login.", placeholder="Enter Key")

    if st.button("Login"):
        if authenticate(password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid Key")

    st.image("amtopm.jpeg", caption="#AMmeetsPM")


if __name__ == "__main__":

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_page()
    else:
        # Define the tabs
        tabs = st.tabs(["RSVP", "Event Timeline", "Testimonials", "Photo Gallery"])

        # Home Tab
        with tabs[0]:
            st.header("We are delighted to invite you to our wedding!")
            # RSVP Form
            with st.expander("RSVP", expanded=False):
                with st.form(key='rsvp_form'):
                    name = st.text_input("Full Name", placeholder="e.g., John Doe")
                    email = st.text_input("Email Address", placeholder="e.g., john.doe@gmail.com")
                    st.write('Select the dates you can attend')
                    attending_23rd = st.checkbox('23rd November - Kolkata')
                    attending_24th = st.checkbox('24th November - Kolkata')
                    attending_26th = st.checkbox('26th November - Mumbai')
                    counter = int(st.number_input("Additional guests count", min_value=0, max_value=3, step=1, key="counter"))
                    song = st.text_input("Your favorite wedding Jam", placeholder="e.g., Die With A Smile, by Bruno Mars and Lady Gaga")


                    # Submit button
                    submit_button = st.form_submit_button(label='Submit RSVP')

                    if submit_button:

                        if name and email and (attending_23rd or attending_24th or attending_26th):
                            # Process the form data (e.g., save to a database or send an email)
                            # Get current UTC time and convert to EST
                            current_time = datetime.now(est).isoformat(timespec='milliseconds')

                            rsvp_record = {
                                'datetime': current_time,
                                'name': name,
                                'email': email,
                                'attending_23rd': attending_23rd,
                                'attending_24th': attending_24th,
                                'attending_26th': attending_26th,
                                'guests': counter,
                                'song': song
                            }
                            save_rsvp(rsvp_record)
                            st.write(f"Thank you for your RSVP, {name}!")
                            st.write(f"Email: {email}")

                        else:
                            st.error("Please provide your name, email, and select at least one date")

            st.video("invite.MP4", format="video/mp4", autoplay=True, muted=False, loop=True)

        # Event Timeline Tab
        with tabs[1]:
            st.header("Event Timeline")
            st.write("---")

            # Timeline content
            timeline_data = [
                {"date": "23rd November 2025: 10:00 AM IST", "title": "Haldi - ঘাই হলুদ",
                 "description": "A splash of sunshine", "attire": "Attire: Bright Shades"},
                {"date": "23rd November 2025: 07:00 PM IST", "title": "Cocktail - ককটেল",
                 "description": "Raising a toast to the beginning of forever", "attire": "Attire: Glitz & Glam"},
                {"date": "24th November 2025: 07:00 PM IST", "title": "Bengali Wedding - বাঙালি হিন্দু বিবাহ",
                 "description": "Traditional bengali wedding", "attire": "Attire: Traditional"},
                {"date": "26th November 2025: 07:00 PM IST", "title": "Bou Bhat - বউ ভাত",
                 "description": "A post-wedding ritual hosted by the groom's family",
                 "attire": "Attire: Bright Shades"},
            ]

            # Build the timeline
            st.markdown('<div class="timeline">', unsafe_allow_html=True)

            for i, event in enumerate(timeline_data):
                st.markdown(f'''
                <div>
                    <div class="date">{event['date']}</div>
                    <div class="content">
                        <h3>{event['title']}</h3>
                        <p>{event['description']}</p>
                        <p>{event['attire']}</p>
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
                    else:
                        st.write(f"**{testimonial['name']}**")
                        st.write(testimonial['testimonial'])

                    # Define emoji reactions
                    emojis = {"👍": "Like", "❤️": "Love", "😂": "Funny"}
                    # Initialize session state for reactions
                    if "reactions" not in st.session_state:
                        st.session_state.reactions = {emoji: 0 for emoji in emojis}
                    # Display reaction buttons
                    cols = st.columns(len(emojis))  # Create columns for each emoji
                    for i, (emoji, label) in enumerate(emojis.items()):
                        if cols[i].button(emoji):
                            st.session_state.reactions[emoji] += 1  # Increment count
                    reaction_str = " ".join(f"{emoji} {count}" for emoji, count in st.session_state.reactions.items())
                    st.write(reaction_str)
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
                                'anonymous': anonymous,
                                'reaction': ""
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

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()


