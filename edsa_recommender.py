"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
from streamlit_option_menu import option_menu

# Data handling dependencies
import pandas as pd
import numpy as np
import os
import re

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model
from PIL import Image
import base64

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')


# Background settings
logo = Image.open('resources/imgs/Logo.jpg')
st.set_page_config(page_title='LunaPix', page_icon=logo)

@st.cache_data
def get_img_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return base64.b64encode(image_data).decode()

image = get_img_as_base64('resources/imgs/background.jpg')
image1 = get_img_as_base64('resources/imgs/Logo.jpg')


background_image = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{image}");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: scroll;
color: black;
display : flex;
justify-content: centre;
align-items: centre;
}}

[data-testid="stSidebar"] {{
background-image: url("data:image/png;base64,{image1}");
background-size: fit;
background-position: center;
background-repeat: no-repeat;
}}
</style>"""
st.markdown(background_image, unsafe_allow_html=True)


#made with streamlit info
hide_st_style = """
            <style>
            #MainMenu {visibility: show;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# -------------------------------------------------------------------

# User account information
user_email = st.text_input('Enter your email address to create an account:')
user_password = st.text_input('Enter your password:', type='password', key='password')
confirm_password = st.text_input('Confirm your password:', type='password', key='confirm_password')

# Validate email format
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
if not re.match(email_pattern, user_email):
    st.warning("Please enter a valid email address.")
    st.stop()

# Validate password match
if user_password != confirm_password:
    st.warning("Passwords do not match. Please confirm your password.")
    st.stop()

# Age validation
user_age = st.number_input('Please enter your age', min_value=1, max_value=150, step=1)
if user_age < 16:
    st.warning("Sorry, this app is intended for users aged 16 and above. You are not eligible.")
    st.stop()

# Account creation
if st.button("Create Account"):
    st.success(f"Account for {user_email} created successfully!")

# -------------------------------------------------------------------

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview", "Analysis", "About Us", "Contact Us" ]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")


    if page_selection == "About Us":
        st.title("Abous Us")

        selected = option_menu(
            menu_title = None,
            options = ["Star-Arc Labz", "Team", "About the App"],
            icons = ["company", "person", "app_indicator"], #https://icons.getbootstrap.com/
            orientation = "horizontal"
        )


        if selected == "Star-Arc Labz":
            st.subheader("Star-Arc Labz")
            st.markdown(open('resources/pages/Who_we_are.md').read())
            st.markdown(open('resources/pages/Mission_statement.md').read())
            st.markdown(open('resources/pages/Vision.md').read())
            st.markdown(open('resources/pages/LunaPix_vision.md').read())



        if selected == "Team":
            st.subheader("Meet Our Team")



            def display_team_member(image_path, member_name, contact_info, role):
                st.image(image_path, caption=member_name, width=200)
                st.write(f"**Name:** {member_name}")
                st.write(f"**Contact Information:** {contact_info}")
                st.write(f"**Role:** {role}")
                st.write("---")

            def about_us():
                st.title("About Us")

            path_to_images_folder = ("resourses/imgs")

            the_team = [
                {'image_file': 'Bonani.jpg', 'name': 'Bonani Mkhari', 'contact_info': 'bonanimkhari@gmail.com', 'role': 'Team Lead'},
                {'image_file': 'Mulalo.jpg', 'name': 'Mulalo Manthanda', 'contact_info': 'manthadamulalo@gmail.com', 'role': 'Project Manager'},
                {'image_file': 'Lucie.jpg', 'name': 'Lucpah Nekati', 'contact_info': 'nekatilpi@gmail.com', 'role': 'Software Developer'},
                {'image_file': 'Lesego.png', 'name': 'Lesego Maponyane', 'contact_info': 'lesegomoraladi@gmail.com', 'role': 'Data Scientist'},
                {'image_file': 'Prince.jpg', 'name': 'Prince Kala', 'contact_info': 'kala33prince@gmail.com', 'role': 'Machine Learning Engineer'},
                {'image_file': 'Mpho.jpg', 'name': 'Mpho Sesinyi', 'contact_info': 'mphoses@hotmail.com', 'role': 'Data Engineer'},
            ]

            for member in the_team:
                image_path = os.path.join(path_to_images_folder, member['image_file'])
                display_team_member(image_path, member['name'], member['contact_info'], member['role'])


        if selected == "About the App":
            st.subheader("LunaPix")
            st.markdown(open('resources/pages/About_LunaPix.md').read())
            st.markdown(open('resources/pages/LunaPix_key_features.md').read())
            st.markdown(open('resources/pages/Why_LunaPix.md').read())
            st.markdown(open('resources/pages/LunaPix_vision.md').read())


# -------------------------------------------------------------------
    
    if page_selection == "Analysis":
        st.title("Exploratory Data Analysis")
        st.write("Behind the Scenes: Understanding Movie Preferences through EDA")

        selected =  option_menu(
            menu_tile =  None,
            options = ["Insights", "Movie Titles Overview"],
            icons = ["database-fill-check", "film"], #https://icons.getbootstrap.com/
            orientation = "horizontal"
        )

        if selected ==  "Insights":
            st.title("Behind The Scenes")       

            if st.checkbox("Top 10 users by number of ratings"):
                st.title("The Top 10 Users by Number of Ratings")
                st.image("resources/visuals/topuser.png", use_column_width=True)


            if st.checkbox("Top 20 movies viewed by users"):
                st.title("Top 20 movies viewed by users")
                st.image("resources/visuals/topviewed.png", use_column_width=True)


            if st.checkbox("Number of movies per director"):
                st.title("Top 10 directors and their movie counts")
                st.image("resources/visuals/directormovies.png", use_column_width=True)


            if st.checkbox("Top 10 Directors with Highest Rated Movies"):
                st.title("Top 10 Directors with Highest Rated Movies")
                st.image("resources/visuals/topdirectors.png", use_column_width=True)

            if st.checkbox("Top 10 Directors with Worst Rated Movies"):
                st.title("Top 10 Directors with Worst Rated Movies")
                st.image("resources/visuals/worstdirectors.png", use_column_width=True)


            if st.checkbox("Top 10 Highest Rated Movies"):
                st.title("The Top 10 Highest Rated Movies")
                st.image("resources/visuals/topmovies.png", use_column_width=True)


            if st.checkbox("Top 10 Worst Rated Movies"):
                st.title("The Top 10 Worst Rated Movies")
                st.image("resources/visuals/worstmovies.png", use_column_width=True)


            if st.checkbox("Most common genres"):
                st.title("Most common genres")
                st.image("resources/visuals/genres.png", use_column_width=True)

            
    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
