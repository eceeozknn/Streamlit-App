import json
import time
import base64
import openai
import requests
import streamlit as st

from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Recipe Recommender",
                   page_icon=":cook:")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(f"""
                <style>.stApp {{
                background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
                background-size: cover
                              }}
                </style>
                 """,
                unsafe_allow_html=True
                )

with st.sidebar:
    choose = option_menu("Recipe Recommender", ["Home", "Starter", "Main Course", "Dessert"],
                         icons=["house", "dot", "dot", "dot"],
                         menu_icon="justify", default_index=0,
                         styles={"container": {"padding": "5!important", "background-color": "#fafafa"},
                                 "icon": {"color": "black", "font-size": "25px"}, 
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                                 "nav-link-selected": {"background-color": "#7EB02E"},
                                }
                        )

def header(Q1=None, Q2=None, Q3=None, Q4=None, food_type=None):

    header = st.container()
    model_training = st.container()
    form = st.form("Preference")

    with header:        
        url = requests.get("https://assets1.lottiefiles.com/packages/lf20_p8xtmag7.json")
        url_json = dict()
        if url.status_code == 200:
            url_json = url.json()
        else:
            print("Error in the URL")

        st_lottie(url_json,
                # change the direction of our animation
                reverse = True,
                # height and width of animation
                height = 200,  
                width = 700,
                # speed of animation
                speed = 0.75,  
                # means the animation will run forever like a gif, and not as a still image
                loop = True,  
                # quality of elements used in the animation, other values are "low" and "medium"
                quality = "high",
                # THis is just to uniquely identify the animation
                key = "Cook" 
                )

        with form:
            flavor = form.text_input(Q1)
            desired_ingredients = form.text_input(Q2)
            allergies = form.text_input(Q3)
            calorie = form.slider(Q4, min_value=10, max_value=1500, value=500, step=1)   
            submitted = form.form_submit_button("Get ready for your recipe!")

        if submitted == True:
            with model_training:
                
                prompt = f"Can you suggest a recipe with {flavor} flavor in type of {food_type}, that contains the ingredients: {desired_ingredients} but not including the {allergies}, approximately {calorie} calorie for one meal? Write name of the recipe at first lines, than ingredients with  list and preparation with step by step."

                API_KEY = "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"
                openai.api_key = API_KEY
                model = "text-davinci-002"
                response = openai.Completion.create(prompt = prompt, 
                                                    model = model,
                                                    max_tokens = 1000,
                                                    temperature = 0.2,
                                                    n = 1)
               
                st.subheader("Your recipe is:")

                progress_bar = st.progress(0)

                for percent_complete in range(100):
                    time.sleep(0.1)
                    progress_bar.progress(percent_complete + 1)
                
                for result in response.choices:
                    st.write(result.text)

question_1 = "What type of flavor are you looking for?"
question_2 = "What ingredients do you want?"
question_3 = "Do you have any allergies or intolerance? If so, what ingredients should be avoided?"
question_4 = "Plesase enter your calorie limit?"


def Main_page():
    add_bg_from_local("confetti.png") 
    header = st.container()
    with header:
    
        st.markdown("<h1 style='text-align: center; color: #ED3125;'>RECIPE RECOMMENDER</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>In this app, you can get recipe recommendations according to your wishes!</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: center; color: #6FAC0D;'>Please choose your category from sidebar.</h5>", unsafe_allow_html=True)

        url = requests.get("https://assets3.lottiefiles.com/packages/lf20_p1bmwqtk.json")
        url_json = dict()
                       
        if url.status_code == 200:
            url_json = url.json()
        else:
            print("Error in the URL")

        st_lottie(url_json,
                # change the direction of our animation
                reverse=True,
                # height and width of animation
                height=500,  
                width=700,
                # speed of animation
                speed=0.85,  
                # means the animation will run forever like a gif, and not as a still image
                loop=True,  
                # quality of elements used in the animation, other values are "low" and "medium"
                quality='high',
                # THis is just to uniquely identify the animation
                key='Meal' 
                )


def Starter():
    add_bg_from_local("confetti.png") 
    st.markdown("<h1 style='text-align: center; color: #ED3125;'>STARTER RECOMMENDER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Please make your selections for your starter recipe.</h3>", unsafe_allow_html=True) 
    header(Q1=question_1, Q2=question_2, Q3=question_3, Q4=question_4, food_type="starter")


def Main_Course():
    add_bg_from_local("confetti.png") 
    st.markdown("<h1 style='text-align: center; color: #ED3125;'>MAIN COURSE RECOMMENDER</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Please make your selections for your main course recipe.</h3>", unsafe_allow_html=True)    
    header(Q1=question_1, Q2=question_2, Q3=question_3, Q4=question_4, food_type="main course")


def Dessert():
    add_bg_from_local("confetti.png") 
    st.markdown("<h1 style='text-align: center; color: #ED3125;'>DESSERT RECOMMENDER </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Please make your selections for your dessert recipe.</h3>", unsafe_allow_html=True)
    header(Q1=question_1, Q2=question_2, Q3=question_3, Q4=question_4, food_type="dessert")


page_names_to_funcs = {"MAIN PAGE": Main_page,
                       "STARTER": Starter, 
                       "MAIN COURSE": Main_Course, 
                       "DESSERT": Dessert
                      }

if choose == "Home":
    page_names_to_funcs["MAIN PAGE"]()

elif choose == "Starter":
    page_names_to_funcs["STARTER"]()

elif choose == "Main Course":
    page_names_to_funcs["MAIN COURSE"]()

elif choose == "Dessert":
    page_names_to_funcs["DESSERT"]()