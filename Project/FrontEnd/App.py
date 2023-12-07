import streamlit as st

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh;
    margin: 0;
    padding: 0;
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


set_png_as_page_bg('Project/BACKGROUND.png')

# Create columns with specified widths
# with st.form("my_form"):
#     # Change text color using HTML in markdown
#     st.markdown('<p style="text-align: center; color: black;">Configuration</p>', unsafe_allow_html=True)
#     # Example of adding a label in black using markdown
#     st.markdown('<p style="color: black;">Name:</p>', unsafe_allow_html=True)
#     name = st.text_input('')
#     gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
#     country = st.selectbox('Country', ['Country 1', 'Country 2', 'Country 3'])
#     favorite_color = st.color_picker('Favorite Color')
#     season = st.selectbox('Season', ['Summer', 'Fall', 'Winter', 'Spring'])
#     chapters = st.slider('Number of Chapters', 3, 15)
#     choices = st.slider('Number of Choices', 2, 5)
#
#     # Every form must have a submit button.
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#        st.write("slider", slider_val, "checkbox", checkbox_val)
#
#     # if st.button('Submit'):
#     #     # Process the form data here
#     #     st.success('Form Submitted')
#     #
#     # st.markdown('</div>', unsafe_allow_html=True)

# Your HTML code
html_form = """
<div class="config-form">
    <div class="config-form">
            <div class="text-center">
                <h2>Configuration Form</h2>
            </div>
            <div class="scrollable-content">
        <!-- All form elements go here -->
            </div>
            <form class="mt-4" id="myForm" onsubmit="return validateForm(event);" action="prologue.html" method="POST">
                <div class="scrollable-content">
                    <div class="form-group col-6 mx-auto">
                        <label for="name">Name:</label>
                        <input type="text" class="form-control" id="name" placeholder="Enter your name" required>
                    </div>

                    <div class="form-group col-6 mx-auto">
                        <label for="gender">Gender:</label>
                        <select class="form-control" id="gender" required>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div class="form-group col-6 mx-auto">
                        <label for="country">Country:</label>
                        <div id="country-container"></div>
                    </div>

                    <div class="form-group col-6 mx-auto">
                        <label for="color">Favorite Color:</label>
                        <input type="color" class="form-control" id="color" required>
                    </div>

                    <div class="form-group col-6 mx-auto">
                        <label for="season">Season:</label>
                        <select class="form-control col-6" id="season" required>
                            <option value="" disabled selected>Choose a preferred season</option>
                            <option value="summer">Summer</option>
                            <option value="fall">Fall</option>
                            <option value="winter">Winter</option>
                            <option value="spring">Spring</option>
                        </select>
                    </div>

                    <div class="form-group col-6 mx-auto">
                        <label for="chapters">Number of Chapters:</label>
                        <input type="number" class="form-control" id="chapters" min="3" max="15" placeholder="Choose between 3 and 15 chapters" required>
                        <span id="error-message" style="color: red;"></span>
                    </div>

                    <div class="form-group mb-4 col-6 mx-auto">
                        <label for="choices">Number of Choices:</label>
                        <input type="number" class="form-control" id="choices" min="2" max="5" placeholder="Choose between two and five choices" required>
                        <span id="choices-error-message" style="color: red;"></span>
                    </div>
                </div>

                <div class="text-center">
                    <button type="submit" id="startbutton" class="btn btn-primary">Start</button>
                </div>
            </form>
        </div>
</div>
"""

# Embed the HTML form in the Streamlit app
st.markdown(html_form, unsafe_allow_html=True)

bin_stre = get_base64_of_bin_file('Project/paper.jpeg')
css="""
<style>
    .stApp {
    [data-testid="stForm"] {
    position: relative;
    background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.2)), url("data:image/png;base64,%s");
    background-size: cover;
    border-radius: 10px;
    margin: auto;
    max-width: 800px;
    box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.35);
    padding-bottom: 20px;
    }
</style>
""" % bin_stre
st.write(css, unsafe_allow_html=True)