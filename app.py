import streamlit as st
from PIL import Image
from model import predict
import base64

st.set_page_config(page_title="Potato Disease Classification", page_icon="🥔")


def display_preventive_measures(predicted_disease):
    preventive_measures = {
        "Early_blight": {
            "measures": [
                "Apply fungicides containing copper or chlorothalonil.",
                "Remove infected leaves to prevent spread.",
                "Rotate crops to avoid disease buildup in soil."
            ],
            "resources": [
                "- [Article: Early Blight Management](https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_veg_potato_2.html)",
                "- [Video: Early Blight Prevention(Hindi)](https://youtu.be/kCo2U3PJIik?si=N5auv0g9L-yDhXPV)"
            ]
        },
        "Late_blight": {
            "measures": [
                "Use fungicides containing chlorothalonil or maneb.",
                "Avoid overhead watering to reduce humidity levels.",
                "Remove infected plants and destroy them."
            ],
            "resources": [
                "- [Article: Late Blight Management](https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_veg_potato_2.html)",
                "- [Video: Late Blight Prevention(Hindi)](https://youtu.be/xZG9U-x6ufw?si=yK4svetMh9shqpp4)"
            ]
        },
        "Potato__healthy": {
            "measures": ["No preventive measures required.", "Keep watering the plants. "], 
            "resources": [ "- [Here's a song you could listen to ](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"]
        }
    }

    st.markdown("<style>.preventive-measures {font-size: 18px;}</style>", unsafe_allow_html=True)
    st.markdown("<div class='preventive-measures'>", unsafe_allow_html=True)
    st.write("### Here are some preventive measures you can take :")
    for measure in preventive_measures.get(predicted_disease, {}).get("measures", []):
        st.write(f"##### - {measure}")

    st.write("### You can further read for the prevention measures here :")
    for resource in preventive_measures.get(predicted_disease, {}).get("resources", []):
        link_text, link_url = resource.split("](")
        link_text = link_text[1:]
        link_url = link_url[:-1]
        st.markdown(f'<a style="font-size: 20px;" href="{link_url}" target="_blank">{link_text}</a>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# @st.cache_data
# def get_img(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# @st.cache(allow_output_mutation=True)
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# original_title = '<h1 style="font-family: serif; color:white; font-size: 20px;">Streamlit CSS Styling✨ </h1>'
# st.markdown(original_title, unsafe_allow_html=True)


# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20240104/pngtree-green-wave-aesthetic-countryside-vector-illustration-of-an-abstract-eco-farm-image_13893034.png");
    background-size: 100vw 100vh; 
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.sidebar.title("About")
st.sidebar.write("This Streamlit app is designed for potato disease classification.")
st.sidebar.write("It uses a convolutional neural network (CNN) to predict whether a potato leaf is infected or not.")
st.sidebar.write("Creators:")
st.sidebar.write("- Harshit Kumar Singh ")
st.sidebar.markdown("- [LinkedIn](https://in.linkedin.com/in/harshit-kumar-singh-183a8226a)")
st.sidebar.write("- Prathum Pandey")
st.sidebar.markdown("- [Github](https://github.com/PrathumP)")
# st.sidebar.write("- <a href='https://github.com/PrathumP'>Github</a>")
st.sidebar.write("- Abhinav Areliya")
st.sidebar.markdown("- [Github](https://github.com/abhinav4-123)")
st.sidebar.write(" You can fork the repo and contribute to it. ")

st.markdown(background_image, unsafe_allow_html=True)

st.write("# Potato Disease Classification")
st.write("")
st.write("#### This tool is aimed to predict if a potato leaf is infected or not using CNN")
st.write("")
st.write("#### Upload an image of a potato leaf to classify its disease.")

file_up = st.file_uploader("Choose an image", type=["jpg"])

if file_up is not None:
    image = Image.open(file_up)
    image_width = 500
    # left_co, cent_co,last_co = st.columns(3)
    # with cent_co:
    #     st.image(image, caption='Uploaded Image',  width=image_width, use_column_width=True)
    st.image(image, caption='Uploaded Image', width=image_width, use_column_width=False)
    st.write("")

    labels = predict(file_up)

    sorted_labels = sorted(labels.items(), key=lambda x: x[1], reverse=True)

    st.write("### Predictions:")
    for label, score in sorted_labels:
        st.write(f" #### **{label.capitalize()}**: {score*100:.4f}%")
        st.progress(score )

    predicted_disease = sorted_labels[0][0]
    display_preventive_measures(predicted_disease)

