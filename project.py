import streamlit as st
import py_avataaars as pa
from PIL import Image
import base64
import os
import matplotlib.pyplot as plt
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Helper function to create the avatar safely
def create_avatar(options):
    try:
        avatar = pa.PyAvataaar(
            style=getattr(pa.AvatarStyle, options['style']),
            skin_color=getattr(pa.SkinColor, options['skin_color']),
            top_type=getattr(pa.TopType, options['top_type']),
            hair_color=getattr(pa.HairColor, options['hair_color']),
            mouth_type=getattr(pa.MouthType, options['mouth_type']),
            eye_type=getattr(pa.EyesType, options['eye_type']),
            eyebrow_type=getattr(pa.EyebrowType, options['eyebrow_type']),
            accessories_type=getattr(pa.AccessoriesType, options['accessories_type']),
            clothe_type=getattr(pa.ClotheType, options['clothe_type']),
            clothe_graphic_type=getattr(pa.ClotheGraphicType, options['clothe_graphic_type'])
        )
        return avatar
    except Exception as e:
        st.error(f"Error creating avatar: {str(e)}")
        return None

# Helper function to allow image downloads
def imagedownload(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as image_file:
            b64 = base64.b64encode(image_file.read()).decode()
            href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download Avatar</a>'
            return href
    else:
        st.error("Image file not found!")
        return ""

# Function to plot personality traits
def plot_personality(traits):
    labels = list(traits.keys())
    values = list(traits.values())
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, values, color='skyblue')
    ax.set_title("Personality Traits")
    ax.set_ylabel("Scores")
    ax.set_ylim(0, 100)
    st.pyplot(fig)

# Load NLP model and tokenizer
@st.cache_resource
def load_nlp_model():
    model_name = "Minej/bert-base-personality"  # Public model
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

# NLP-based personality analysis
def nlp_personality_analysis(description):
    model, tokenizer = load_nlp_model()
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    scores = torch.softmax(outputs.logits, dim=1).detach().numpy()[0]
    traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    return {trait: round(float(score * 100), 2) for trait, score in zip(traits, scores)}


# Page title
st.markdown("""
# Advanced Avatar & Personality Insights

Design a custom avatar, and get accurate insights into your personality traits using modern frameworks.

---
""")

# Sidebar customization
st.sidebar.header("Customize Your Avatar")

# Avatar options
avatar_options = {
    "style": st.sidebar.selectbox("Style", ("CIRCLE", "TRANSPARENT")),
    "skin_color": st.sidebar.selectbox("Skin Color", ["TANNED", "YELLOW", "PALE", "LIGHT", "BROWN", "DARK_BROWN", "BLACK"]),
    "top_type": st.sidebar.selectbox("Head Top", ["NO_HAIR", "LONG_HAIR_BOB", "SHORT_HAIR_THE_CAESAR", "HIJAB"]),
    "hair_color": st.sidebar.selectbox("Hair Color", ["AUBURN", "BLACK", "BLONDE", "BROWN", "RED", "SILVER_GRAY"]),
    "clothe_type": st.sidebar.selectbox("Clothing Type", ["BLAZER_SHIRT", "GRAPHIC_SHIRT", "HOODIE"]),
    "clothe_graphic_type": st.sidebar.selectbox("Clothing Graphic", ["BAT", "DIAMOND", "HOLA", "SKULL"]),
    "mouth_type": st.sidebar.selectbox("Mouth Type", ["DEFAULT", "SMILE", "TONGUE", "SERIOUS"]),
    "eye_type": st.sidebar.selectbox("Eye Type", ["DEFAULT", "HAPPY", "SURPRISED", "WINK"]),
    "eyebrow_type": st.sidebar.selectbox("Eyebrow Type", ["DEFAULT", "RAISED_EXCITED", "FROWN_NATURAL"]),
    "accessories_type": st.sidebar.selectbox("Accessories", ["DEFAULT", "SUNGLASSES", "PRESCRIPTION_01"])
}

# Create and render avatar
st.subheader("Your Customized Avatar")
avatar = create_avatar(avatar_options)
if avatar:
    avatar.render_png_file("avatar.png")
    image = Image.open("avatar.png")
    st.image(image, caption="Your Avatar")
    st.markdown(imagedownload("avatar.png"), unsafe_allow_html=True)

# Personality analysis section
st.markdown("---")
st.header("Advanced Personality Insights")
st.write("**Describe yourself briefly by entering a description of your personality below:**")

# Free text input for NLP analysis
description = st.text_area("Describe your personality in a few sentences:")
traits = {}

if description:
    st.write("Analyzing your personality description...")
    traits = nlp_personality_analysis(description)
    st.write("Personality Traits (from NLP):", traits)
    plot_personality(traits)

st.markdown("---")
st.markdown("**App Built with Streamlit and Python**")
