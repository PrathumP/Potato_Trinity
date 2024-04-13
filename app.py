import streamlit as st
from PIL import Image
from model import predict
import base64

def display_preventive_measures(predicted_disease):
    preventive_measures = {
        "early_blight": {
            "measures": [
                "Apply fungicides containing copper or chlorothalonil.",
                "Remove infected leaves to prevent spread.",
                "Rotate crops to avoid disease buildup in soil."
            ],
            "resources": [
                "- [Article: Early Blight Management](https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_veg_potato_2.html)",
                "- [Video: Early Blight Prevention](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
            ]
        },
        "late_blight": {
            "measures": [
                "Use fungicides containing chlorothalonil or maneb.",
                "Avoid overhead watering to reduce humidity levels.",
                "Remove infected plants and destroy them."
            ],
            "resources": [
                "- [Article: Late Blight Management](https://agritech.tnau.ac.in/crop_protection/crop_prot_crop%20diseases_veg_potato_2.html)",
                "- [Video: Late Blight Prevention](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
            ]
        },
        "healthy": {
            "measures": ["No preventive measures required.", "Keep watering the plants. "], 
            "resources": []
        }
    }

    st.write("### Here are some preventive measures you can take :")
    for measure in preventive_measures.get(predicted_disease, {}).get("measures", []):
        st.write(f"- {measure}")

    st.write("### You can further read for the prevention measures here :")
    for resource in preventive_measures.get(predicted_disease, {}).get("resources", []):
        st.markdown(resource)

st.set_page_config(page_title="Potato Disease Classification", page_icon="🥔")

@st.cache_data
def get_img(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

local_image_path = 'bgg.png'  # Make sure the image is in the same folder
img = get_img(local_image_path)

page_bg_img = f"""
[data-testid="stAppViewContainer"] {{ background-image: url("data:image/png;base64,{img}"); background-size: cover; }}
"""

st.title("Potato Disease Classification")
st.write("")
st.write("This tool is aimed to predict if a potato leaf is infected or not using CNN")
st.write("")
st.write("Upload an image of a potato leaf to classify its disease.")

file_up = st.file_uploader("Choose an image", type=["jpg"])

if file_up is not None:
    image = Image.open(file_up)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")

    labels = predict(file_up)

    sorted_labels = sorted(labels.items(), key=lambda x: x[1], reverse=True)

    st.write("### Predictions:")
    for label, score in sorted_labels:
        st.write(f"**{label.capitalize()}**: {score}%")
        st.progress(score / 100) 

    predicted_disease = sorted_labels[0][0]
    display_preventive_measures(predicted_disease)
